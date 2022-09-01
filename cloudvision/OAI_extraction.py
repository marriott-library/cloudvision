import os
import sys
import io
import urllib.request
from django.http import HttpResponse
import requests
import shutil
import json
from xml.dom import minidom
import ssl
import base64
import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from io import BytesIO
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

# Thinking about merging this class into OAISearchData

def get_sets(oai_uri):
    uri =  oai_uri + "?verb=ListSets"
    context = ssl._create_unverified_context()

    dom = minidom.parse(urllib.request.urlopen(uri, context = context)) # parse the data

    sets = dom.getElementsByTagName('set')
    
    set_dict = {}

    for s in sets:
        set_spec = s.getElementsByTagName('setSpec')[0].firstChild.nodeValue
        set_name = s.getElementsByTagName('setName')[0].firstChild.nodeValue
        set_dict.update({set_spec : set_name})

    return set_dict

def get_set_records(oai_uri, set_id):
    uri =  oai_uri + "?verb=ListRecords&metadataPrefix=oai_dc&set=" + set_id
    context = ssl._create_unverified_context()

    dom = minidom.parse(urllib.request.urlopen(uri, context = context)) # parse the data
    
    records = dom.getElementsByTagName('record')
    
    record_list = []

    # Problem. Must change from Identifier
    for record in records:
        identifier = record.getElementsByTagName('identifier')[0].firstChild.nodeValue
        record_list.append(identifier)
    
    return record_list

# responsible for condencing metadata into OAI link, source file location, 
    # and ocr_data location. CSV is downloaded to local machine. 
def get_OAI_CSV(oai_uri, set_name, record_list): 
    base =  oai_uri + "?verb=GetRecord&metadataPrefix=oai_dc&identifier="
    context = ssl._create_unverified_context()
    row = ["metadata_link ", "file_location ", "ocr_data "]

    # metadata = open(os.environ['HOME'] + "/" + set_name + '.csv', 'w')
    metadata = open('./' + set_name + '.csv', 'w')

    # create the csv writer object
    csvwriter = csv.writer(metadata)
    csvwriter.writerow(row)

    for record in record_list: 
        uri = base + record

        row = [] 
        row.append(uri)
        row.append("")

        csvwriter.writerow(row)
    
    metadata.close()



# responsible for condencing metadata into a few important fields, source file location, 
    # and ocr_data location. CSV is downloaded to the local machine. 
def get_set_CSV(oai_uri, set_name, record_list): 
    base =  oai_uri + "?verb=GetRecord&metadataPrefix=oai_dc&identifier="
    context = ssl._create_unverified_context()

    row = ["identifier ", "collection ", "creator ", "date ", "format ", "language ", 
        "place ", "publisher ", "subject ", "title ", "type ", "file_location ", "ocr_data "]


    # metadata = open(os.environ['HOME'] + "/" + set_name + '.csv', 'w')
    metadata = open('./' + set_name + '.csv', 'w')

    # create the csv writer object
    csvwriter = csv.writer(metadata)
    csvwriter.writerow(row)

    for record in record_list: 
        uri = base + record

        dom = minidom.parse(urllib.request.urlopen(uri, context = context)) # parse the data
            
        row = []

        identifiers = dom.getElementsByTagName("dc:identifier")
        # metadataPrefixes = dom.getElementsByTagName("dc:metadataPrefix")

        collections = dom.getElementsByTagName("dc:collection")
        creators = dom.getElementsByTagName("dc:creator")
        dates = dom.getElementsByTagName("dc:date")
        formats = dom.getElementsByTagName("dc:format")
        languages = dom.getElementsByTagName("dc:language")
        places = dom.getElementsByTagName("dc:place")
        publishers  = dom.getElementsByTagName("dc:publisher")
        subjects = dom.getElementsByTagName("dc:subject")
        titles = dom.getElementsByTagName("dc:title")
        types = dom.getElementsByTagName("dc:type")

        if identifiers: 
            identifier = identifiers[0].firstChild.nodeValue
        else: 
            identifier = ""

        # if metadataPrefixes: 
        #     metadataPrefix = metadataPrefixes[0].firstChild.nodeValue
        # else:
        #     metadataPrefix = ""
        
        if collections:
            collection = collections[0].firstChild.nodeValue
        else: 
            collection = ""
        
        if creators:
            creator = creators[0].firstChild.nodeValue
        else: 
            creator = ""
        
        if dates:
            date = dates[0].firstChild.nodeValue
        else: 
            date = ""

        if formats:
            format = formats[0].firstChild.nodeValue
        else: 
            format = ""
        
        if languages:
            language = languages[0].firstChild.nodeValue
        else: 
            language = ""
        
        if places:
            place = places[0].firstChild.nodeValue
        else: 
            place = ""
        
        if publishers:
            publisher = publishers[0].firstChild.nodeValue
        else: 
            publisher = ""

        if subjects:
            subject = subjects[0].firstChild.nodeValue
        else: 
            subject = ""

        if titles:
            title = titles[0].firstChild.nodeValue
        else: 
            title = ""

        if types:
            type = types[0].firstChild.nodeValue
        else: 
            type = ""

        row.append(identifier)
        # row.append(metadataPrefix)
        row.append(collection)
        row.append(creator)
        row.append(date)
        row.append(format)
        row.append(language)
        row.append(place)
        row.append(publisher)
        row.append(subject)
        row.append(title) 
        row.append(type)
        
        # for file_location
        row.append("")
        # for ocr_data
        row.append("")

        csvwriter.writerow(row)

    metadata.close()
        


    #     xml_link = urllib.request.urlopen(uri)
    #     # load and parse the file
    #     xmlTree = ET.parse(xml_link)
    #     root = xmlTree.getroot()

    #     row = []

    #     for elem in xmlTree.iter():
    #         prefix, has_namespace, postfix = elem.tag.partition('}')
    #         if has_namespace:
    #             elem.tag = postfix  # strip all namespaces


    #     if root.find("collection"):
    #         collection = root.find("collection").text
    #         row.append(collection)
    #     else:
    #         row.append("")
        
    #     if root.find("creator"):
    #         creator = root.find("creator").text
    #         row.append(creator)
    #     else:
    #         row.append("")

        
    #     if root.find("date"):
    #         date = root.find("date").text
    #         row.append(date)
    #     else:
    #         row.append("")

    #     if root.find("format"):
    #         format = root.find("format").text
    #         row.append(format)
    #     else:
    #         row.append("")

    #     if root.find("language"):
    #         language = root.find("language").text
    #         row.append(language)
    #     else:
    #         row.append("")
        
    #     if root.find("place"):
    #         place = root.find("place").text
    #         row.append(place)
    #     else:
    #         row.append("")
        
    #     if root.find("publisher"):
    #         publisher = root.find("publisher").text
    #         row.append(publisher)
    #     else:
    #         row.append("")
        
    #     if root.find("subject"):
    #         subject = root.find("subject").text
    #         row.append(subject)
    #     else:
    #         row.append("")
        
    #     if root.find("title"):
    #         title = root.find("title").text
    #         row.append(title)
    #     else:
    #         row.append("")
        
    #     if root.find("type"):
    #         type = root.find("type").text
    #         row.append(type)
    #     else:
    #         row.append("")

    #     csvwriter.writerow(row)

    # metadata.close()







    # elemList = []
    
    # for elem in xmlTree.iter():
    #     prefix, has_namespace, postfix = elem.tag.partition('}')
    #     if has_namespace:
    #         elem.tag = postfix  # strip all namespaces

    #     elemList.append(elem.tag)

    # now I remove duplicities - by convertion to set and back to list
    # elemList = list(set(elemList))
    # open a file for writing

    # metadata = open('./' + set_name + '.csv', 'w')

    # # create the csv writer object

    # csvwriter = csv.writer(metadata)
    # csvwriter.writerow(elemList)

    # for record in record_list: 
    #     uri = base + record
    #      xml_link = urllib.request.urlopen(uri)
    #     # load and parse the file
    #     xmlTree = ET.parse(xml_link)

        # for i in range(len(elemList)):
        #     info = []

        #     info.append()

        #     name = member.find('Name').text
        #     resident.append(name)
        #     PhoneNumber = member.find('PhoneNumber').text
        #     resident.append(PhoneNumber)
        #     EmailAddress = member.find('EmailAddress').text
        #     resident.append(EmailAddress)
        #     Address = member[3][0].text
        #     address_list.append(Address)
        #     City = member[3][1].text
        #     address_list.append(City)
        #     StateCode = member[3][2].text
        #     address_list.append(StateCode)
        #     PostalCode = member[3][3].text
        #     address_list.append(PostalCode)
        #     resident.append(address_list)
        #     csvwriter.writerow(resident)
        # Resident_data.close()

    # Just printing out the result
    # print(elemList)
    
    
    

# ------------------------Extraction Helper Methods-----------------

# param -> a directory path containing pdf documents
# converts pdf's to images and saves to specified dir
# returns -> ? 
def pdf2jpeg(doc_dir, image_dir): 

    for filename in os.listdir(doc_dir):
        if filename.endswith(".pdf"):
            
            # gets path of  pdf doc
            doc = os.path.join(doc_dir, filename) 

            # creates a directory with same name as dco for images
            output_image = os.path.join(image_dir, filename[0 : len(filename)-4])
            os.mkdir(output_image)

            images_from_path = convert_from_path(doc, output_folder=output_image, fmt='jpeg')
        else:
            continue

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('ascii')

# def OAI2pdf(starting_id, ending_id,  OAI_uri, pdf_output):
#     cwd = os.getcwd()
#     idNumber = starting_id
    
#     while idNumber < ending_id:
#         # Contacts UDN api and gets response for the article request with the current id we've gotten to (using idNumber)
#         # responseString = "https://api.lib.utah.edu/udn/v1/docs/id/"

#         responseString =  OAI_uri + "?verb=GetRecord&metadataPrefix=oai_dc&identifier="
#         responseString += str(idNumber)
#         response = requests.get(responseString)
#         responseSplit = response.content.__str__()
#         responseSplit = responseSplit.split("\"")

#         # Searches for the pdf url among the api response, we'll use that pdfStr to download the pdf
#         pdfStr = ""
#         for strg in responseSplit:
#             chars = list(strg)
#             if len(chars) > 2:
#                 if chars[len(chars) - 3] == 'p' and chars[len(chars) - 2] == 'd' and chars[len(chars) - 1] == 'f':
#                     pdfStr = strg

#         # Remove backslashes from pdf url that we need to get rid of
#         for _ in pdfStr:
#             pdfStr = pdfStr.replace('\\', '')
#         url = pdfStr

#         # Specifies the path that we'll be downloading too
#         pdf_file =  pdf_output + str(idNumber) + ".pdf"
        
#         open(pdf_file,'x')
#         # With the url of the pdf, open the file and write that file to the outputFile location
#         with urllib.request.urlopen(url) as response, open(pdf_file, 'wb') as out_file:
#             shutil.copyfileobj(response, out_file)
        
#         idNumber = idNumber + 1
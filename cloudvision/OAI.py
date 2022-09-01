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
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import mimetypes


class OAISearchData:
    def __init__(self):
        self.base_uri = ""
        self.set_list = {}
        self.set_name = ""
        self.record_list = []

    def add_base_uri(self, base_uri):
        self.base_uri = base_uri

    def add_set_list(self, set_list):
        self.set_list = set_list

    def add_set_name(self, set_name):
        self.set_name = set_name

    def add_record_list(self, record_list):
        self.record_list = record_list

    # Thinking about merging this class into OAISearchData
    def get_sets(self):
        if not self.base_uri:
            # throw error
            return

        uri = self.base_uri + "?verb=ListSets"
        context = ssl._create_unverified_context()

        dom = minidom.parse(urllib.request.urlopen(uri, context=context))  # parse the data

        sets = dom.getElementsByTagName('set')

        set_dict = {}

        for s in sets:
            set_spec = s.getElementsByTagName('setSpec')[0].firstChild.nodeValue
            set_name = s.getElementsByTagName('setName')[0].firstChild.nodeValue
            set_dict.update({set_spec: set_name})

        self.add_set_list(set_dict)
        return set_dict

    def get_set_records(self):
        if not self.base_uri and self.set_name:
            # throw error
            return

        uri = self.base_uri + "?verb=ListRecords&metadataPrefix=oai_dc&set=" + self.set_name
        context = ssl._create_unverified_context()

        dom = minidom.parse(urllib.request.urlopen(uri, context=context))  # parse the data

        records = dom.getElementsByTagName('record')

        record_list = []

        # Problem. Must change from Identifier
        for record in records:
            identifier = record.getElementsByTagName('identifier')[0].firstChild.nodeValue
            record_list.append(identifier)

        self.add_record_list(record_list)

        return record_list

    # responsible for condencing metadata into OAI link, source file location,
    # and ocr_data location. CSV is downloaded to local machine.
    def get_OAI_df(self):
        if not self.base_uri or self.record_list:
            # thorow error
            return

        base = self.base_uri + "?verb=GetRecord&metadataPrefix=oai_dc&identifier="
        context = ssl._create_unverified_context()

        data = [[]]

        for record in self.add_record_list:
            uri = base + record

            row = []
            row.append(uri)
            row.append("")
            data.append(row)

        dataframe = pd.DataFrame(data, columns=['metadata_link', 'file_location', 'ocr_data'])
        return dataframe

    # responsible for condencing metadata into a few important fields, source file location,
    # and ocr_data location. CSV is downloaded to the local machine.
    def get_set_df(self):
        # if not self.base_uri or self.record_list:
        #     # throw error
        #     return
        base = self.base_uri + "?verb=GetRecord&metadataPrefix=oai_dc&identifier="
        context = ssl._create_unverified_context()

        data = [[]]

        for record in self.record_list:
            uri = base + record

            dom = minidom.parse(urllib.request.urlopen(uri, context=context))  # parse the data

            row = []

            identifiers = dom.getElementsByTagName("dc:identifier")
            collections = dom.getElementsByTagName("dc:collection")
            creators = dom.getElementsByTagName("dc:creator")
            dates = dom.getElementsByTagName("dc:date")
            formats = dom.getElementsByTagName("dc:format")
            languages = dom.getElementsByTagName("dc:language")
            places = dom.getElementsByTagName("dc:place")
            publishers = dom.getElementsByTagName("dc:publisher")
            subjects = dom.getElementsByTagName("dc:subject")
            titles = dom.getElementsByTagName("dc:title")
            types = dom.getElementsByTagName("dc:type")

            if identifiers:
                identifier = identifiers[0].firstChild.nodeValue
            else:
                identifier = ""

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

            data.append(row)

        dataframe = pd.DataFrame(data, columns=['identifier', 'collection', 'creator', 'date', 'format', 'language',
                                                'place', 'publisher', 'subject', 'title', 'type', 'file_location',
                                                'ocr_data'])

        print(dataframe.to_string())
        print("\n \n")

        return dataframe

    def get_default_df():
        data = [[]]
        dataframe = pd.DataFrame(data, columns=['identifier', 'collection', 'creator', 'date', 'format', 'language',
                                                'place', 'publisher', 'subject', 'title', 'type', 'file_location',
                                                'ocr_data'])

        return dataframe

import os
import sys
import io
import urllib.request
import requests
import shutil
import json
import base64
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from io import BytesIO
from PIL import Image
import time
import cv2
import pytesseract
from time import sleep
import file_handler
from cloudvision.settings import BASE_DIR, DATA_DIR
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)


# OCR Analysis Module
import ocr_analyse as ocr_analyse

# params <- ocr framework id, directory of pdf documents (only required field),
    # derivative image folder (empty or NULL to generate one),
    # and an ocr output directory (empty or NULL to generate one).
def extract(framework_id, doc_dir = "", der_dir = "", out_dir = "", images = False):
    # Start Logging OCR process
    sys.stdout = open(os.path.join(doc_dir, "ocr_log.log"), 'w')
    if doc_dir == "" and der_dir == "":
        print("No input for document directory or derivative directory")
        return

    out_path = ""

    if not images:
        if not os.path.isdir(doc_dir):
            # Error message -- not a valid input
            print("Invalid directory path")
            return

        # Generates directories if there was no or incorrect derivative dir path input
        if der_dir == "" or os.path.isdir(der_dir):
            doc_dir_parent = os.path.abspath(os.path.join(doc_dir, os.pardir))
            der_dir = os.path.join(doc_dir_parent, "image_output")
            os.mkdir(der_dir)

        out_path = os.path.abspath(os.path.join(doc_dir, os.pardir))

        file_handler.pdf2jpeg(doc_dir, der_dir)
    else:
        if not os.path.isdir(der_dir):
            # Error message -- not a valid input
            print("Invalid directory path")
            return

        out_path = os.path.abspath(os.path.join(der_dir, os.pardir))

    # Generates directories if there was no or incorrect out dir path input
    if out_dir == "" or os.path.isdir(out_dir):
        out_dir = os.path.join(out_path, "ocr_output")
        os.mkdir(out_dir)

    # grab api_hit limit from config file
    # read config file
    with open(BASE_DIR+'/appconfig.json', 'r') as myfile:
        data = myfile.read()

    # parse file
    obj = json.loads(data)

    # get api_hit_limit
    hits_per_min = int(obj['hits_per_min'])

    # get key secret
    google_subscription_key = obj["keys"]['GOOGLE_APPLICATION_CREDENTIALS']
    azure_subscription_key = obj["keys"]['COMPUTER_VISION_SUBSCRIPTION_KEY']

    if framework_id == "azure":
        service_name = "Azure"
        input_files, output_files, results = azure_extr(der_dir, out_dir, hits_per_min, azure_subscription_key)
    elif framework_id == "google_vision":
        service_name = "Google Vision"
        input_files, output_files, results = google_vision_extract(der_dir, out_dir, hits_per_min, google_subscription_key)
    elif framework_id == "tesseract":
        service_name = "Tesseract"
        input_files, output_files, results = tesseract_extract(der_dir, out_dir, hits_per_min)
    # sys.stdout.close()
    return service_name, input_files, output_files, results

# Param <- given an input directory (image_dir) and an output directory (out_dir)
    # the function will OCR, using azure, any images in input directroy
    # to json and store each json file in output directory.
# Returns nothing
def azure_extr(images_dir, out_dir, hits_per_min, subscription_key):
    input_files = []
    output_files = []
    results = []

    hits_per_min = 19
    api_hits = 0
    start_time = time.time()

    for root, image_dirs, image_files in os.walk(images_dir):

        #iterates over all dirs conaining images
        for image_name in image_dirs:
            # print(image_name)

            count = 0; # incrament image page

            # creates dir with the same as image and pdf for json files
            json_dir = out_dir
            json_dir = os.path.join(json_dir, image_name)
            os.makedirs(json_dir, exist_ok=True)


            # gets single image dir path
            image_dir = os.path.join(root, image_name)
            for filename in os.listdir(image_dir):
                #might be useless if
                if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):

                    # gets file for single image file
                    image = os.path.join(image_dir, filename)

                    input_files.append(image)
                    # Read the image into a byte array
                    # resize image to below 4200
                    src = cv2.imread(image, cv2.IMREAD_UNCHANGED)

                    # percent by which the image is resized
                    scale_percent = 1
                    # width > height MAX
                    if max(src.shape[1], src.shape[0]) >= 4200:
                        scale_percent = 4200 / max(src.shape[1], src.shape[0])
                    # calculate the 50 percent of original dimensions
                    width = int(src.shape[1] * scale_percent )
                    height = int(src.shape[0] * scale_percent)

                    # dsize
                    dsize = (width, height)

                    # resize image
                    output = cv2.resize(src, dsize)

                    cv2.imwrite(image, output)
                    image_data = open(image, "rb").read()
                    src = cv2.imread(image, cv2.IMREAD_UNCHANGED)
                    print(src.shape[0],src.shape[1])
                    time_dif = time.time() - start_time
                    if api_hits == hits_per_min and time_dif < 60:
                        # time.sleep(time_dif)
                        # Rest 60 seconds before calling next API:
                        print("Wait 60 Seconds before Process next image")
                        time.sleep(60)
                        start_time = time.time()
                        # reset API
                        api_hits = 0

                    word_infos = azure_image_extract(image_data, subscription_key)
                    word_infos["output_id"] = image_name
                    results.append(word_infos)

                    api_hits = api_hits + 1

                    # creates file path for json file
                    json_file = os.path.join(json_dir, filename[0 : len(filename)-4] + "(" + str(count) + ")" + ".json")
                    output_files.append(json_file)
                    count = count + 1

                    # writes json
                    with open(json_file, "w") as outfile:
                        outfile.write(json.dumps(word_infos, indent = 4))
                else:
                    continue
    return input_files, output_files, results

# Param <- given an input directory (image_dir) and an output directory (out_dir)
    # the function will OCR any images using google vision and put them in input directroy
    # to json and store them in output directory.
# Returns nothing
def google_vision_extract(image_derivatives, output_dir, hits_per_min, subscription_key):
    input_files = []
    output_files = []
    results = []


    api_hits = 0
    start_time = time.time()

    for root, image_dirs, image_files in os.walk(image_derivatives):
        #iterates over all dirs conaining images
        for image_name in image_dirs:

            count = 0; # incrament image page

            # creates dir with the same as image and pdf for json files
            json_dir = output_dir
            json_dir = os.path.join(json_dir, image_name)
            os.makedirs(json_dir, exist_ok=True)

            # gets single image dir path
            image_dir = os.path.join(root, image_name)

            for filename in os.listdir(image_dir):
                #might be useless if
                if filename.endswith(".png") or filename.endswith(".jpg"):
                    print(filename)

                    # gets file for single image file
                    image = os.path.join(image_dir, filename)

                    input_files.append(image)

                    image_data = file_handler.encode_image(image)

                    time_dif = time.time() - start_time
                    if api_hits == hits_per_min and time_dif < 60:
                        time.sleep(time_dif)
                        start_time = time.time()

                    response = google_vision_image_extract(image_data, subscription_key)
                    response["output_id"] = image_name
                    api_hits = api_hits + 1

                    # creates file path for json file
                    json_file = os.path.join(json_dir, filename[0 : len(filename)-4] + "(" + str(count) + ")" + ".json")

                    results.append(response)
                    output_files.append(json_file)

                    count = count + 1

                    # writes json
                    with open(json_file, "w") as outfile:
                        outfile.write(json.dumps(response, indent = 4))
                else:
                    continue
    return input_files, output_files, results


def tesseract_extract(images_dir, out_dir, hits_per_min):
    input_files = []
    output_files = []
    results = []


    api_hits = 0
    start_time = time.time()

    for root, image_dirs, image_files in os.walk(images_dir):

        #iterates over all dirs conaining images
        for image_name in image_dirs:

            count = 0; # incrament image page

            # creates dir with the same as image and pdf for json files
            json_dir = out_dir
            json_dir = os.path.join(json_dir, image_name)
            os.makedirs(json_dir, exist_ok=True)


            # gets single image dir path
            image_dir = os.path.join(root, image_name)

            for filename in os.listdir(image_dir):
                #might be useless if
                if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    print(filename)

                    # gets file for single image file
                    image = os.path.join(image_dir, filename)

                    input_files.append(image)
                    # Read the image into a byte array
                    # image_data = open(image, "rb").read()
                    image_data = cv2.imread(image)

                    time_dif = time.time() - start_time
                    if api_hits == hits_per_min and time_dif < 60:
                        time.sleep(time_dif)
                        start_time = time.time()


                    ocr_dict = tesseract_image_extract(image_data)
                    ocr_dict["output_id"] = image_name
                    api_hits = api_hits + 1

                    # ocr_dict = pytesseract.image_to_data(image_data, output_type=pytesseract.Output.DICT)

                    # creates file path for json file
                    json_file = os.path.join(json_dir, filename[0 : len(filename)-4] + "(" + str(count) + ")" + ".json")

                    results.append(ocr_dict)
                    output_files.append(json_file)


                    count = count + 1

                    # writes json
                    with open(json_file, "w") as outfile:
                        outfile.write(json.dumps(ocr_dict, indent = 4))
                else:
                    continue
    return input_files, output_files, results

# Takes image data, and returns dictionary
def tesseract_image_extract(image_data):

    ocr_dict = pytesseract.image_to_data(image_data, output_type=pytesseract.Output.DICT)

    ocr_array = file_handler.tesseract_json_reformat(ocr_dict)

    ocr_text = [obj["text"] for obj in ocr_array]
    ocr_str = ' '.join(ocr_text)
    ocrs = [ocr_str]

    ocr_analyse_results = ocr_analyse.analysis_ocr_from_txts(ocrs)
    ocr_dict = {'data': ocr_array, "ocr_analyse_results": ocr_analyse_results}

    return ocr_dict

def google_vision_image_extract(image_data, subscription_key):
    URL = "https://vision.googleapis.com/v1/images:annotate?key="+subscription_key

    data = {
    "requests": [
        {
        "features": [
            {
            "maxResults": 50,
            "type": "LANDMARK_DETECTION"
            },
            {
            "maxResults": 50,
            "type": "FACE_DETECTION"
            },
            {
            "maxResults": 50,
            "type": "OBJECT_LOCALIZATION"
            },
            {
            "maxResults": 50,
            "type": "LOGO_DETECTION"
            },
            {
            "maxResults": 50,
            "type": "LABEL_DETECTION"
            },
            {
            "maxResults": 50,
            "type": "DOCUMENT_TEXT_DETECTION"
            },
            {
            "maxResults": 50,
            "type": "SAFE_SEARCH_DETECTION"
            },
            {
            "maxResults": 50,
            "type": "IMAGE_PROPERTIES"
            },
            {
            "maxResults": 50,
            "type": "CROP_HINTS"
            }
        ],
        "image": {
            "content": image_data
        },
        "imageContext": {
            "cropHintsParams": {
            "aspectRatios": [
                0.8,
                1,
                1.2
            ]
            }
        }
        }
    ]
    }
    googleJSONResponse = requests.post(URL, json=data)

    response = googleJSONResponse.json()

    # Add ocr accuracy info to google vision response data
    ocr_analyse_results = ocr_analyse.analysis_ocr_from_json(response,
                                                                ["responses", 0, "fullTextAnnotation",
                                                                "text"])
    response["ocr_analyse_results"] = ocr_analyse_results

    return response

def azure_image_extract(image_data, subscription_key):
    endpoint = "https://mlibdidocrinitialtesting.cognitiveservices.azure.com/"
    ocr_url = endpoint + "vision/v3.1/ocr"

    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {'language': 'unk', 'detectOrientation': 'true'}
    # put the byte array into your post request
    try:
        response = requests.post(ocr_url, headers=headers, params=params, data = image_data)
        print(response.json())
        response.raise_for_status()
        analysis = response.json()
    except Exception as ex:
        response = requests.post(ocr_url, headers=headers, params=params, data=image_data)
        print(response.json())
        raise ex

    # Extract the word bounding boxes and text.
    line_infos = [region["lines"] for region in analysis["regions"]]
    word_infos = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                word_infos.append(word_info)
    word_infos

    # Add ocr performance data to azure response data
    ocr_list = [obj["text"] for obj in word_infos]
    ocr_str = ' '.join(ocr_list)
    ocrs = [ocr_str]

    ocr_analyse_results = ocr_analyse.analysis_ocr_from_txts(ocrs)
    word_infos = {'data': word_infos, "ocr_analyse_results": ocr_analyse_results}

    return word_infos

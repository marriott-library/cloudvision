import os
import sys
from django.http import FileResponse
import io
import urllib.request
from django.http import HttpResponse
import requests
import shutil
from wsgiref.util import FileWrapper
import json
from xml.dom import minidom
import ssl
import base64
import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from io import BytesIO
from PIL import Image
import mimetypes
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)


def df2tsv(df, filename, filepath):
    tsv_filepath = filepath + filename + '.tsv'
    tsv_file = open(tsv_filepath, 'w')
    df.to_csv(tsv_file, sep='\t')
    tsv_file.close()

    return filename, tsv_filepath


def pdf2jpeg(doc_dir, image_dir):
    for filename in os.listdir(doc_dir):
        if filename.endswith(".pdf"):
            # gets path of  pdf doc
            doc = os.path.join(doc_dir, filename)
            # creates a directory with same name as doc for images
            output_image = os.path.join(image_dir, filename[0: len(filename) - 4])
            os.makedirs(output_image, exist_ok=True)
            images_from_path = convert_from_path(doc, 200, output_folder=output_image, fmt='jpeg')

        else:
            continue


def download_file(filename, filepath):
    # fill these variables with real values
    fl_path = filepath
    filename += ".tsv"

    fl = open(fl_path, 'r')
    # mime_type, _ = mimetypes.guess_type(fl_path)
    mime_type = 'text/tsv'
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def download_zip(filename, filepath):
    response = HttpResponse(FileWrapper(open(filepath, 'rb')), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + filename + '.zip'
    return response
    # zip_file = open(filepath, 'rb')
    # return FileResponse(zip_file)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('ascii')


def tesseract_json_reformat(ocr_dict):
    level = ocr_dict["level"]
    page_num = ocr_dict["page_num"]
    block_num = ocr_dict["block_num"]
    par_num = ocr_dict["par_num"]
    line_num = ocr_dict["line_num"]
    word_num = ocr_dict["word_num"]
    left = ocr_dict["left"]
    top = ocr_dict["top"]
    width = ocr_dict["width"]
    height = ocr_dict["height"]
    conf = ocr_dict["conf"]
    txt = ocr_dict["text"]

    data = []
    for x in range(len(level)):
        text = {}
        text["level"] = level[x]
        text["page_num"] = page_num[x]
        text["block_num"] = block_num[x]
        text["par_num"] = par_num[x]
        text["line_num"] = line_num[x]
        text["word_num"] = word_num[x]
        text["left"] = left[x]
        text["top"] = top[x]
        text["widt"] = width[x]
        text["height"] = height[x]
        text["conf"] = conf[x]
        text["text"] = txt[x]

        data.append(text)

    return data

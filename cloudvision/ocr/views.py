from cloudvision.settings import MEDIA_ROOT, DATA_DIR
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, FileUploadForm
from django.views.generic.base import TemplateView
from django.core import serializers
from django.forms.models import model_to_dict
from django.conf import settings
from ocr.models import Log
import requests
import urllib.request
import shutil
import zipfile
import io
import ssl
import os
import json
import math
import ocr_functions
import datetime
from datetime import timezone
import base64
import uuid
import pandas as pd
import OAI_extraction
from OAI import OAISearchData

import file_handler
from google.cloud import vision
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

# Questionable design choice. Spent alot of time considering using the django model and session data.
    # Temporarily decided against both.
    # search_data is a global variable that gets passed around from view to view during a session.
search_data = OAISearchData()


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was created for ' + form.cleaned_data.get('username'))
            return redirect('login')
    context = {'form':form}
    return render(request, 'ocr/register.html', context)


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('oai')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('login')
			else:
				messages.info(request, 'Username OR password is incorrect')
		context = {}
		return render(request, 'ocr/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('ascii')


@login_required(login_url='login')
def oai(request):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context
        cwd = os.getcwd()

    if request.method == "POST":
        if request.POST['Modifytag'] == 'nextPage':
            return redirect('/import')

        # fix naming in df2tsv. Generally clean up.
        search_dataframe = search_data.get_set_df()
        file_path = "./" + search_data.set_name
        file_info = file_handler.df2tsv(search_dataframe, search_data.set_name, file_path)
        response = file_handler.download_file(file_info[0], file_info[1])
        # response = OAI_extraction.get_set_tsv(oai_endpoint, set_name, record_list)
        return response

    return render(request, 'ocr/oai.html', {})


def redirect_page(request):
    return redirect('/import')

def template_tsv(request, filename=''):
    if filename != '':
        print(MEDIA_ROOT + "template.tsv")
        response = file_handler.download_file('template.tsv', MEDIA_ROOT + 'template.tsv')
        return response
    else:
        return render(request, 'ocr/import_tsv.html')


@login_required(login_url='login')
def import_tsv(request):
    if request.method == "POST":
        if request.FILES['the_file'].name.endswith('.tsv'):
            FileForm = FileUploadForm(request.POST, request.FILES)
            ocr_framework = request.POST.get('framework_select', None)
            # Check that file is valid
            if FileForm.is_valid():
                # Bind file to model
                job_id = handle_uploaded_file(request.FILES['the_file'], request.FILES['the_file'].name, ocr_framework,
                                              request)
                return HttpResponse(job_id)
        else:
            return render(request, 'ocr/import_tsv.html', {'form': FileUploadForm(), 'correct': False})
    return render(request, 'ocr/import_tsv.html', {'form': FileUploadForm(), 'correct': True})


def handle_uploaded_file(f, name, ocr_framework, request):
    print("top of handle_upload_file")
    # Capture start time
    run_start_time = datetime.datetime.now(timezone.utc).astimezone()
    filename = os.path.join(DATA_DIR, name)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if f != "":
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    unique_folder = str(uuid.uuid4())
    doc_dir = DATA_DIR + '/' + unique_folder + '/ocr_data' + '/doc_dir/'
    os.makedirs(os.path.dirname(doc_dir))
    df = pd.read_csv(filename, sep='\t', header=0)
    file_locations = df["file_location"].values.tolist()
    for file in file_locations:
        r = requests.get(file, stream=True)
        file_name = file.rsplit('/', 1)[-1]
        with open(doc_dir + file_name, 'wb') as f:
            f.write(r.content)
    service_name, input_files, output_files, results = ocr_functions.extract(ocr_framework, doc_dir=doc_dir)
    # Capture end time
    run_end_time = datetime.datetime.now(timezone.utc).astimezone()
    # Calculate run time
    run_time = int(round((run_end_time - run_start_time).total_seconds() * 1000))
    # Insert into DB
    # HttpRequest.POST
    user_id = request.user
    # Path to TSV file
    input_file = filename
    # ocr result unique_folder id
    output_file = unique_folder
    # ocr result in JSON format
    results = json.dumps(results)
    ocr_result = results
    # service Run Start time
    run_start_time = str(run_start_time)
    # service Run End time
    run_end_time = str(run_end_time)
    # length of Process Time in million seconds
    run_time = run_time
    log = Log(service_name=service_name, user_id=user_id, input_file=input_file, output_file=output_file,
              ocr_result=ocr_result, run_start_time=run_start_time, run_end_time=run_end_time, run_time=run_time)
    log.save()
    shutil.make_archive(DATA_DIR + '/' + unique_folder + '/ocr_data', 'zip',
                        DATA_DIR + '/' + unique_folder + '/ocr_data/')
    print("after")
    return log.id


@login_required(login_url='login')
def ocr_download(request, uuid):
    response = file_handler.download_zip('ocr_data', DATA_DIR + '/' + uuid + '/ocr_data.zip')
    return response


@login_required(login_url='login')
def results(request, job_id = None):
    # Process OCR through quick run button
    if request.method == "POST":
        ocr_framework = request.POST['action']
        input_file = request.POST['input_file']
        file_exist = os.path.exists(input_file)
        # Check that file is valid
        if file_exist:
            handle_uploaded_file("", input_file, ocr_framework, request)
        else:
            print("Input File does not exist in original path anymore")

    if job_id is None:
        logs = get_all_jobs(request)
        jobs = {}
        for job in logs:
            if not job["input_file"] in jobs.keys():
                jobs[job["input_file"]] = {"name":job["input_file"],"Azures": [], "Google_Visions": [], "Tesseracts":[], "last_updated": job['created']}
            # TODO: add AWS here
            if(job["service_name"] == "Azure"):
                jobs[job["input_file"]]["Azures"].append(job)
            elif job["service_name"] == "Google Vision":
                jobs[job["input_file"]]["Google_Visions"].append(job)
            elif job["service_name"] == "Tesseract":
                jobs[job["input_file"]]["Tesseracts"].append(job)
            if job['created'] > jobs[job["input_file"]]["last_updated"]:
                jobs[job["input_file"]]["last_updated"] = job['created']
        return render(request, 'ocr/results.html', {'jobs':jobs.values})
    else:
        log = get_job_by_id(request, job_id)
        if get_job_by_id(request, job_id) is None:
            return HttpResponse("No Job with that ID")
        uuid = log.output_file
        ctx = log
        job_headers = [f.name for f in Log._meta.get_fields()]
        readable_headers = ["ID", "Created By", "Service", "Input File", "Output File Id", "Result", "Created",
                            "Run Time (ms)"]
        values = {}
        for item in job_headers:
            values[item] = getattr(ctx, item)

        # return full lists of image urls
        img_list = {}
        for root, image_dirs, image_files in os.walk(DATA_DIR + "/" + uuid + "/ocr_data/image_output"):
            for image_name in image_dirs:
                img_list[image_name] = []
                image_dir = os.path.join(root, image_name)
                for filename in os.listdir(image_dir):
                    # might be useless if
                    if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                        img_url = settings.STATIC_DATA_URL + "/"+uuid+"/ocr_data/image_output/"+image_name+"/"+filename
                        img_list[image_name].append(img_url)
        # Display username for user
        # values["user_id_id"] = log.user_id.get_username()
        # Display run time in seconds
        values["run_time"] = str(values["run_time"] / 1000) + " S"
        return render(request, 'ocr/jobs.html', {'headers': readable_headers, "vals": values, 'img_urls': img_list, "uuid": uuid,"job_id": job_id})


# Function responsible for loading set of sets after OAI endpoint is entered
def load_sets(request):
    oai_endpoint = request.POST['oai_endpoint']
    sets = OAI_extraction.get_sets(oai_endpoint)
    search_data.add_base_uri(oai_endpoint)
    search_data.add_set_list(sets)
    return JsonResponse(sets, safe=False)


# Method responsible for loading list of records after set is selectecd.
def load_records(request):
    set_name = request.POST['set_name']
    oai_endpoint = search_data.base_uri
    search_data.add_set_name(set_name)
    record_ids = OAI_extraction.get_set_records(oai_endpoint, set_name)
    search_data.add_record_list(record_ids)
    return JsonResponse(record_ids, safe=False)


@login_required(login_url='login')
# Load all Logs from DB, return , return JSON result,
def get_all(request):
    logs = Log.objects.all()
    return JsonResponse(list(logs.values()), safe=False)


@login_required(login_url='login')
# Load Log record from DB by Id, return JSON result,
def get(request, job_id):
    log = Log.objects.get(pk=job_id)
    log = model_to_dict(log)
    return JsonResponse(log, safe=False)

@login_required(login_url='login')
# Load Log record from DB by Id, API, return Object
def get_job_by_id(request, job_id):
    log = Log.objects.get(pk=job_id)
    return log


@login_required(login_url='login')
# Load Log record from DB by Id, API, return Objects
def get_all_jobs(request):
    logs = Log.objects.values('id', 'user_id_id', 'created','service_name','input_file')
    return logs

# Cloudvision: A toolkit for Digital Libraries

## What is Cloudvision
Cloudvision is a a toolkit for Digital Libraries to explore and evaluate the quality of the collections OCR data, that also provides libraries with easy to use tools to use Google Vision and Microsoft Computer Vision services to enrich their Digital Collection descriptive and technical metadata.

## Running Cloudvision

### Database Setup
  1. For windows user: Checkout Database file from gitlab using "git checkout cloudvision\\container-data\\db.sqlite3" in Project Root Folder
  2. For Linux user:  Checkout Database file from gitlab using "git checkout cloudvision/container-data/db.sqlite3" in Project Root Folder

### Cloud Service Credentials Setup
  1. Google Vision: open and modify file appconfig.json under cloudvision folder, place your subscription_key under GOOGLE_APPLICATION_CREDENTIALS
  2. Azure: open and modify file appconfig.json under cloudvision folder, place your subscription_key under COMPUTER_VISION_SUBSCRIPTION_KEY

### Option 1: Creating Docker Container
  1. Build the image. Make sure you are in the root folder of the project and run `docker build -t cloudvision .`
  2. For windows user: Run the docker container locally via `docker run -dit -p 8000:8000 --name cloudvision -v ABSOLUTE_PATH\\TO\\PROJECT\\container-data\\:/cloudvision/container-data/ cloudvision`. This will map port 8000 in the docker container to your own computer's port 8000, so you can view the webpage at localhost:8000/login. Also local directory `ABSOLUTE_PATH\TO\PROJECT\container-data` will be allocated as shared folder for DB storage, input files and output results
  3. For Linux user: Run the docker container locally via `docker run -dit -p 8000:8000 --name cloudvision -v ABSOLUTE_PATH/TO/PROJECT/container-data/:/cloudvision/container-data/ cloudvision`. This will map port 8000 in the docker container to your own computer's port 8000, so you can view the webpage at localhost:8000/login. Also local directory `ABSOLUTE_PATH/TO/PROJECT/container-data` will be allocated as shared folder for DB storage, input files and output results

#### Useful commands:
*  To see all images that have been built and stored locally, run `docker images`
*  To see all docker containers that are currently running, run `docker ps`
*  To see all docker containers, even if they aren't running, run `docker ps -all`
*  You can use `docker pull <image name>` to pull an existing image, and `docker rmi <image name>` to delete a (local) image.
*  To clean up and delete unused images and stopped containers, run `docker system prune`. Do this regularly if you are building and/or running docker containers frequently.



### Option 2: Setup Outside of Docker (Windows not supported)
  1. Clone the respository to your local machine
  2. Navigate to the outer cloudvision directory, and run `pip install -r requirements.txt && python -m spacy download en_core_web_md`
  3. Navigate into the inner cloudvision foled, and run `python manage.py runserver 8000`


### Create User Account and Login
  1. Open browser and visit http://localhost:8000/ to be redirected to the login page, create an user account by clicking "Sign Up", login after user account created

### Get TSV File
  a tsv file that contains urls to pdfs in 'file_location' field is required for OCR process, you can download the tsv template from [import page](http://localhost:8000/import) and manually add pdf urls to 'file_location' field or you can create a blank tsv file and manually add single column field 'file_location'.  
  1. If you have a remote OAI Endpoint (e.g. https://collections.lib.utah.edu/oai), you can download tsv file from selected sets and records from [oai page](http://localhost:8000/oai). Some of the downloaded tsv files don't have 'file_location' field value, in this case you still need to manually add urls to the field.
  2. Work with Local PDF: Cloudvision support local PDFs for OCR process, place the local pdf files inside 'container-data' folder and mark it as local url as "http://localhost:8000/data/path/to/folder/pdf_name.pdf" in tsv file for OCR process.

#### Important Note for TSV File
  1. all values in 'file_location' field must be a valid pdf url, if not please fix the invalid url manually or download pdf file to local and make it a local url path.
  2. blank line is not allowed in tsv file.

#### Example of valid tsv file  
the following example has 2 pdf files to process, the first one is a remote resource with url provided. The second one is a local pdf file "No_14_Original_Defendant_s_Exceptions_to_the_Report_of_the_Special_Master_1930.pdf" placed under 'project_root/cloudvision/container-data/pdfs' folder.  


file_location

https://collections.lib.utah.edu/dl_files//c6/11/c611193d8652f0cf62e0817d2eb813f65960c56c.pdf

http://localhost:8000/data/pdfs/No_14_Original_Defendant_s_Exceptions_to_the_Report_of_the_Special_Master_1930.pdf



### Process OCR
Cloudvision supports Google Vision, Azure and Tessearct frameworks for processing OCR, and **fees will apply for the service**.
  1. Visit [import page](http://localhost:8000/import) and upload the tsv file from the previous step, select one of the frameworks from the list,then click "Process Files" button. Process time varies from seconds to minutes and depends on input file size and selected framework. A success message including the link to results will show up after the process has finished.

### View and Download Results
  1. Click "view results" link in the success message to visit the results page, you can download the results as a zip file that includes original pdfs, rendered image files, ocr results in JSON format.
  2. You can access all jobs that were run at [results page](http://localhost:8000/results).


## Dependencies

*  Python
*  pip
*  requests
*  google.cloud
*  pdf2image
*  Django
*  Pillow
*  certifi
*  chardet
*  idna
*  setuptools
*  urllib3
*  matplotlib
*  spacy
*  spacy language model: download en_core_web_md
*  pandas
*  pytessera
*  poppler-utils
*  uuid
*  tesseract-ocr

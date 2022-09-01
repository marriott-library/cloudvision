FROM python:3.9.5-slim-buster

ENV VENV "/venv"
RUN python3 -m venv $VENV
# ENV PATH "$VENV/bin:$PATH"

RUN apt-get -y update
RUN apt-get install -y poppler-utils
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /
COPY . /

RUN pip install --upgrade pip
RUN pip install -r requirements.txt && pip install google-cloud-vision
RUN apt-get update -y
RUN apt-get install -y poppler-utils
RUN apt-get install -y tesseract-ocr

# Download Spacy dictionary model for word reference
RUN python -m spacy download en_core_web_md
CMD ["python", "cloudvision/manage.py", "runserver", "0.0.0.0:8000"]

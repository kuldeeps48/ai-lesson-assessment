# Base image
# FROM --platform=linux/amd64 python:3.11.9-slim
FROM python:3.11.9-slim

RUN apt-get update && apt-get -y install tesseract-ocr libtesseract-dev tesseract-ocr-hin tesseract-ocr-script-deva poppler-utils 

ENV PYTHONUNBUFFERED=1

# Make directory to copy our project there
RUN mkdir /code

WORKDIR /code/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /code/app
COPY .env /code/app

RUN tesseract --list-langs

EXPOSE 8080

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--no-server-header"]

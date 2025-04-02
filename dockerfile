FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install speciesnet

RUN pip install pillow

RUN pip uninstall opencv-python-headless -y

RUN pip install --no-cache-dir opencv-python-headless
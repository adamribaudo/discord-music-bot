# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
# WORKDIR /app
# RUN apt-get install libopus0
COPY requirements.txt requirements.txt
RUN apt-get update -y && apt-get upgrade -y && apt-get install libopus0 -y && \
	pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && \
	apt-get autoremove -y
# RUN pip3 install -r requirements.txt
COPY . .
CMD python3 app.py
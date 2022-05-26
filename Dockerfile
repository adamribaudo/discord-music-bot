# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
COPY requirements.txt requirements.txt
RUN apt-get update -y && apt-get upgrade -y && apt-get install libopus0 -y && \
	pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && \
	apt-get autoremove -y
COPY . .
# CMD python3 app.py
# CMD should be overridden to include an argument containing the bot profile ex: CMD python3 app.py my-bot-name

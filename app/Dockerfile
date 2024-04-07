#Importing base image
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache -r requirements.txt
RUN pip install gunicorn

CMD gunicorn --bind 0.0.0.0:5000 run:app
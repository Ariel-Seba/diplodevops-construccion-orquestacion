# syntax=docker/dockerfile:1
FROM python:3.11-alpine

ADD . /code
WORKDIR /code/src

RUN pip install -r requirements.txt && mkdir uploads
CMD ["python", "app.py"]

# syntax=docker/dockerfile:1
FROM python:3.7.17-alpine3.18

ADD . /code
WORKDIR /code/src

RUN pip install -r requirements.txt && mkdir uploads
CMD ["python", "app.py"]
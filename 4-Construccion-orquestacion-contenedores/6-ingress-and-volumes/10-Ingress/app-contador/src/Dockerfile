# syntax=docker/dockerfile:1
FROM python:3.7.17-alpine3.18

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt
CMD ["python", "app.py"]
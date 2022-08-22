FROM python:3

RUN apt-get update
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
RUN mkdir upload
RUN chmod 644 upload

RUN mkdir upload/tmp
RUN chmod 644 upload/tmp

WORKDIR /app
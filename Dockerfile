FROM python:3

RUN apt-get update
COPY requirements.txt requirements.txt
COPT secrets.json secrets.json
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

WORKDIR /app

FROM python:3.11

WORKDIR /evendy_project

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY evendy_project/ .

EXPOSE 8000
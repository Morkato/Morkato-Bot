FROM python:3.10-slim AS builder
WORKDIR /usr/app
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY morkato morkato
COPY app app
COPY home home
COPY main.py main.py
ENV MORKATO_HOME=/usr/app/home
ENTRYPOINT [ "python3", "main.py" ]
FROM python:3.11.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV DB_HOST localhost
ENV DB_USER postgres
ENV DB_PASSWORD pwd
ENV DB_NAME properties

COPY . .

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0" ]
FROM python:3.11.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV BOT_TOKEN "987654321:AAA-AAAAAA"
ENV ADMIN_IDS "123 231 312"
ENV REDIS_HOST "localhost"
ENV REDIS_PORT "6379"
ENV REDIS_DB "1"
ENV API_URL "http://localhost"
ENV API_PORT "8000"

COPY . .

ENTRYPOINT [ "python", "bot.py" ]
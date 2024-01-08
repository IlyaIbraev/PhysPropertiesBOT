FROM node:20.10.0-slim

WORKDIR /app

COPY ./build .

RUN npm install -g serve

ENTRYPOINT [ "serve", "-s", "." ]
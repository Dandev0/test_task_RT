FROM alpine:3.17
COPY requirements.txt /app/
WORKDIR /app
RUN apt-get update
RUN pip install -r requirements.txt
EXPOSE 30002
COPY . /app
WORKDIR /app

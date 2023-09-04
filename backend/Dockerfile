FROM python:3.11
COPY requirements.txt /app/
WORKDIR /app
RUN apt-get update
RUN pip install -r requirements.txt
EXPOSE 5672
EXPOSE 30001
ENV RABBITMQ_LOGIN=test
ENV RABBITMQ_PASSWORD=test
ENV RABBITMQ_IP=46.146.229.116
ENV RABBITMQ_PORT=5672
COPY . /backend /app
CMD ["python3", "main.py"]

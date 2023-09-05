FROM python:3.11
COPY requirements.txt /app/
WORKDIR /app
RUN apt-get update
RUN pip install -r requirements.txt
EXPOSE 30000
ENV RABBITMQ_LOGIN=test
ENV RABBITMQ_PASSWORD=test
ENV RABBITMQ_IP=46.146.229.116
ENV RABBITMQ_PORT=5672
ENV DATABASE_LOGIN=dandev0
ENV DATABASE_PASSWORD=Apassword_test21
ENV DATABASE_IP=46.146.229.116
ENV DATABASE_PORT=5432
COPY ./servicedb  /app
WORKDIR /app
CMD ["python3", "fast_api_server.py"]

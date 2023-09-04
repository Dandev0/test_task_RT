FROM python:3.11
COPY requirements.txt /app/
WORKDIR /app
RUN apt-get update
RUN pip install -r requirements.txt
EXPOSE 30002
COPY ./frontend /app
CMD ["python3", "flask_server.py"]

from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

"""CREDENTIALS DATABASE POSTGRESQL"""
DATABASE_LOGIN = os.getenv("DATABASE_LOGIN")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_IP = os.getenv("DATABASE_IP")
DATABASE_PORT = os.getenv("DATABASE_PORT")

RABBITMQ_LOGIN = os.getenv("RABBITMQ_LOGIN")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_IP = os.getenv("RABBITMQ_IP")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")


SQLALCHEMY_DATABASE_URL = F"postgresql://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{DATABASE_IP}:{DATABASE_PORT}/call_service"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

HOST = "0.0.0.0"
PORT = "30000"

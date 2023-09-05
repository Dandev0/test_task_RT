from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

"""CREDENTIALS DATABASE POSTGRESQL"""
DATABASE_LOGIN = os.getenv("DATABASE_LOGIN")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_IP = os.getenv("DATABASE_IP")
DATABASE_PORT = os.getenv("DATABASE_PORT")


SQLALCHEMY_DATABASE_URL = F"postgresql://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{DATABASE_IP}:{DATABASE_PORT}/call_service"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

HOST = "0.0.0.0"
PORT = "30000"

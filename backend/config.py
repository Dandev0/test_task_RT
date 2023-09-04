from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

"""CREDENTIALS RABBITMQ"""
RABBITMQ_LOGIN = os.getenv("RABBITMQ_LOGIN")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_IP = os.getenv("RABBITMQ_IP")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
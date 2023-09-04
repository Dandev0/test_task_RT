import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask

load_dotenv(find_dotenv())
secret_key = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.secret_key = secret_key

HOST = '0.0.0.0'
PORT = '30002'
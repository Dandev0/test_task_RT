import logging
import time
from fastapi import FastAPI, Response, Request, Body, BackgroundTasks
import uvicorn
import pika
from pika import exceptions
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URL, HOST, PORT
from sqlalchemy import Column, Integer, Text, UnicodeText, MetaData, Table, insert
from sqlalchemy_utils import PhoneNumberType
import ast
import threading

app = FastAPI()


class Appeal:
    def __init__(self, name, surname, lastname, phone_number, description_appeal, metadata=MetaData(),
                 engine=create_engine(SQLALCHEMY_DATABASE_URL)):
        self.conn = engine.connect()
        self.name = name
        self.surname = surname
        self.last_name = lastname
        self.phone_number = phone_number
        self.description_appeal = description_appeal
        self.model_appeal = Table('appeal', metadata,
                                  Column('id', Integer, primary_key=True, index=True),
                                  Column('name', Text, unique=False, nullable=False),
                                  Column('surname', Text, unique=False, nullable=False),
                                  Column('last_name', Text, unique=False, nullable=False),
                                  Column('phone_number', PhoneNumberType()),
                                  Column('description_appeal', UnicodeText, unique=False, nullable=False),
                                  extend_existing=True
                                  )

    def write_data_to_database(self):
        self.__data_from_appeal = insert(self.model_appeal).values(
            name=self.name,
            last_name=self.last_name,
            surname=self.surname,
            phone_number=self.phone_number,
            description_appeal=self.description_appeal

        )
        self.conn.execute(self.__data_from_appeal)
        self.conn.commit()


class Rabbit_listener:
    def __init__(self, message: str = None):
        self.credentials = pika.PlainCredentials('test', 'test')
        self.parameters = pika.ConnectionParameters(host='46.146.229.116', port=5672, virtual_host='/',
                                                    credentials=self.credentials)
        self.connection = None
        self.channel = None
        self.message = message

    def connect(self):
            try:
                if not self.connection or self.connection.is_closed:
                    self.connection = pika.BlockingConnection(self.parameters)
                    self.channel = self.connection.channel()
                    if self.connection:
                        logging.warning('Connection to RabbitMQ is UP!')
                    self.get_message()

            except pika.exceptions.AMQPConnectionError:
                time.sleep(3)
                logging.warning('Error:\npika.exceptions.AMQPConnectionError\nReconnect to RabbitMQ')
                self.connect()

            except pika.exceptions.ConnectionClosedByBroker:
                time.sleep(3)
                logging.warning('Error:\npika.exceptions.ConnectionClosedByBroker\nReconnect to RabbitMQ')
                self.connect()

            except pika.exceptions.ConnectionWrongStateError as error:
                time.sleep(3)
                logging.warning('Error:\npika.exceptions.ConnectionWrongStateError\nReconnect to RabbitMQ')
                self.connect()

    @staticmethod
    def db_write(ch, method, properties, data):
        str_data = data.decode('utf-8')
        data = ast.literal_eval(str_data)
        Appeal(name=data['name'], surname=data['surname'], lastname=data['last_name'],
               phone_number=data['phone_number'],
               description_appeal=data['description_appeal']).write_data_to_database()

    def get_message(self):
        try:
            self.channel.queue_declare(queue='/dev-queue')
            self.channel.basic_consume(queue='dev-queue',
                                       auto_ack=True,
                                       on_message_callback=self.db_write)
            self.channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            time.sleep(3)
            logging.warning('Error:\npika.exceptions.AMQPConnectionError\nReconnect to RabbitMQ')
            self.connect()

        except pika.exceptions.ConnectionClosedByBroker:
            time.sleep(3)
            logging.warning('Error:\npika.exceptions.ConnectionClosedByBroker\nReconnect to RabbitMQ')
            self.connect()

        except pika.exceptions.ConnectionWrongStateError as error:
            time.sleep(3)
            logging.warning('Error:\npika.exceptions.ConnectionWrongStateError\nReconnect to RabbitMQ')
            self.connect()


def on_startup():
    rabbit_listener_task = Rabbit_listener()
    BackgroundTasks().add_task(func=rabbit_listener_task.connect())


def start_web_server():
    uvicorn.run(app, host=HOST, port=PORT, log_level='debug')


if __name__ == "__main__":
    thread1 = threading.Thread(target=start_web_server)
    thread2 = threading.Thread(target=on_startup)
    thread1.start()
    thread2.start()
    thread1.join(timeout=1)
    thread2.join(timeout=1)

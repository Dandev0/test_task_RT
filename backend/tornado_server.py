import asyncio
import logging
import tornado
import pika
from pika import exceptions
from ast import literal_eval
import time
from config import RABBITMQ_LOGIN, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_IP
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        self.response = {'message' : 'Your request has been received!'}
        request_payload = str(literal_eval(self.request.body.decode('utf-8'))['data'])
        message = request_payload
        send_message_to_rabbit = Rabbit(message=message).send_message()
        self.set_status(send_message_to_rabbit['status_code'])
        json_response = json.dumps(send_message_to_rabbit)
        return self.write(json_response)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler)])


async def start_server():
    app = make_app()
    app.listen(30001)
    await asyncio.Event().wait()


class Rabbit:
    def __init__(self, message: str = None):
        self.credentials = pika.PlainCredentials(RABBITMQ_LOGIN, RABBITMQ_PASSWORD)
        self.parameters = pika.ConnectionParameters(host=RABBITMQ_IP, port=RABBITMQ_PORT, virtual_host='/',
                                               credentials=self.credentials)
        self.connection = None
        self.channel = None
        self.message = message
        self.error = None

    def connect(self):
        try:
            if not self.connection or self.connection.is_closed:
                self.connection = pika.BlockingConnection(self.parameters)
                self.channel = self.connection.channel()
                if self.connection:
                    logging.warning('Connection to RabbitMQ is UP!')

        except exceptions.AMQPConnectionError:
            self.__error = {'message': 'The server was unable to process your request',
                             'description': 'AMQPConnectionError',  "status_code": 502}

        except exceptions.ConnectionClosedByBroker:
            self.__error = {'message': 'The server was unable to process your request',
                             'description': 'ConnectionClosedByBroker',  "status_code": 502}

        except exceptions.ConnectionWrongStateError:
            self.__error = {'message': 'The server was unable to process your request',
                             'description': 'ConnectionWrongStateError', "status_code": 502}


    def send_message(self):
        self.connect()
        if not self.connection:
            return self.__error
        self.channel.basic_publish(exchange='',
                                   routing_key='dev-queue', body=self.message)
        logging.info('Message is sent to Rabbit')
        self.__response_from_rabbit = {"message": "Message is sent to Rabbit",  "status_code": 201}
        return self.__response_from_rabbit


if __name__ == "__main__":
    asyncio.run(start_server())

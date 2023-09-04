import asyncio
import logging
import tornado
import pika
from ast import literal_eval
from backend.config import RABBITMQ_LOGIN, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_IP


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

    def post(self):
        request_payload = str(literal_eval(self.request.body.decode('utf-8'))['data'])
        message = request_payload
        Rabbit(message=message).send_message()


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
        parameters = pika.ConnectionParameters(host=RABBITMQ_IP, port=RABBITMQ_PORT, virtual_host='/',
                                               credentials=self.credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.message = message

    def send_message(self):
        self.channel.basic_publish(exchange='',
                                   routing_key='dev-queue', body=self.message)
        logging.info('Message is sent to Rabbit')


if __name__ == "__main__":
    asyncio.run(start_server())

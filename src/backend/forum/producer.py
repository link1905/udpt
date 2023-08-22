import json
import pika
from django.conf import settings

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=settings.RABBIT_MQ_URL,
                              credentials=pika.credentials.PlainCredentials('udptgroup1', 'udptgroup1'),
                              heartbeat=600,
                              blocked_connection_timeout=300))
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='',
                          routing_key='forum',
                          body=json.dumps(body),
                          properties=properties)

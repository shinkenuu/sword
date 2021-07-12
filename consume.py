import json

import pika

from sword.settings import RABBITMQ_URL, RABBITMQ_EXCHANGE, RABBITMQ_QUEUE


def on_message(channel, method_frame, header_frame, body):
    decoded_body = body.decode()
    message = json.loads(decoded_body)

    print(f"The technician with id {message['user']} performed the task with id {message['id']} on date {message['performed_at']}")

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


parameters = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(RABBITMQ_EXCHANGE)
channel.queue_declare(RABBITMQ_QUEUE)

channel.queue_bind(RABBITMQ_QUEUE, RABBITMQ_EXCHANGE)
channel.basic_consume(RABBITMQ_QUEUE, on_message)

try:
    print("Consuming messages...")
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()

import json
import logging

import pika

from sword.settings import RABBITMQ_URL


def publish(exchange: str, routing_key: str, message: dict):
    parameters = pika.URLParameters(RABBITMQ_URL)
    properties = pika.BasicProperties(
        content_type='application/json',
        delivery_mode=1,
    )

    body = bytes(json.dumps(message), encoding='utf-8')

    logging.debug("Connecting to RabbitMQ at %s", RABBITMQ_URL)
    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()

        logging.info("Publishing @ '%s' -> %s : %s", exchange, routing_key, message)
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
            properties=properties,
        )

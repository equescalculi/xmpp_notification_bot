#!/usr/bin/env python
"""Create a notification and send it to RabbitMQ"""
# Licensed under the MIT License, see LICENSE for details

import json
import pika

from settings import MQ_HOST, MQ_PORT, MQ_USER, MQ_PASSWORD, QUEUE


def notify(group, message):
    """
    Queue a message in RabbitMQ

    Parameters
    ----------
    group : str
        name of the group to which the message is addressed
    message : str
        the message
    """

    # Create a RabbitMQ connection
    credentials = pika.credentials.PlainCredentials(MQ_USER, MQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=MQ_HOST,
        port=MQ_PORT,
        credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)

    # Create a JSON object and send it to RabbitMQ
    data = {}
    data['group'] = group
    data['message'] = message
    channel.basic_publish(exchange='', routing_key=QUEUE,
                          body=json.dumps(data))
    connection.close()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: notify.py [group] [message]")
    else:
        notify(sys.argv[1], sys.argv[2])

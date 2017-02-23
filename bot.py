#!/usr/bin/env python
"""Retrieve messages from RabbitMQ and send the them via XMPP"""
# Licensed under the MIT License, see LICENSE for details

import json
import logging
import pika
from sleekxmpp import ClientXMPP
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from dbschema import Addressee, Group, Membership
from settings import JID, PASSWORD, MQ_HOST, MQ_PORT, MQ_USER, MQ_PASSWORD, QUEUE, DATABASE


class NotificationBot(ClientXMPP):
    """Implement a XMPP Client to send messages"""

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('session_start', self.session_start)

    def session_start(self, event):
        """
        Implement a session_start event handler

        Parameters
        ----------
        event : dict
            event information
        """

        self.send_presence()

    def message_group(self, group, message):
        """
        Send a message to all members of a group

        Parameters
        ----------
        group : str
            name of the group to which the message is addressed
        message : str
            the message
        """

        try:
            # Create the database connection
            engine = create_engine(DATABASE)
            Session = sessionmaker()
            Session.configure(bind=engine)
            session = Session()

            # Query all group names
            groups = [g[0] for g in session.query(Group.name).all()]

            if group in groups:
                # Query all JIDs belonging to a group
                jids = [c.jid for c in session.query(Addressee).join(
                    Membership).join(Group).filter(Group.name == group).all()]
                # Send the message to every addressee in the group
                for jid in jids:
                    self.send_message(mto=jid, mbody=message, mtype='chat')
            else:
                logging.warning("No group named \"%s\" exists", group)
        except SQLAlchemyError:
            logging.error("Unable to query the list of addressees")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

    # Create the RabbitMQ connection
    credentials = pika.credentials.PlainCredentials(MQ_USER, MQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=MQ_HOST,
        port=MQ_PORT,
        credentials=credentials))

    bot = NotificationBot(JID, PASSWORD)

    def callback(ch, method, properties, body):
        """
        Parse the RabbitMQ message and send it via NotificationBot

        A consumer_callback function, see documentation of
        pika.channel.Channel.basic_consume
        """

        try:
            data = json.loads(body)
            bot.message_group(data['group'], data['message'])
        except json.JSONDecodeError:
            logging.error("Unable to parse the RabbitMQ message body")
        except KeyError:
            logging.error("Incomplete JSON data object")

    if bot.connect():
        bot.process()
        while True:
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE)
            channel.basic_consume(callback, queue=QUEUE, no_ack=True)
            channel.start_consuming()

    else:
        logging.error("Unable to connect")

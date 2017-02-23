# xmpp_notification_bot

An experimental XMPP bot that sends out notifications queued in RabbitMQ by
other applications to contacts listed in a database

**WARNING!** This is an early version.

## Goal

The idea behind this project is to have an easy possibility to send out
notifications via XMPP from multiple scripts. E.g., one might be running several
processes on a computer and a human needs to be notified in certain instances.

## Dependencies

 * Python (tested with versions 2.7.13 and 3.6.0)
 * SleekXMPP (tested with version 1.3.1)
 * pika (tested with version 0.10.0)
 * SQLAlchemy (tested with version 1.1.5)
 * RabbitMQ (tested with version 3.6.6)
 * a SQL database (tested with SQLite)

## Usage

 1. Create a file `settings.py` and define all variables like in
    `settings.py.example`.
 2. Create a database for the addressees and their groups
    making use of the example script `createdb.py.example`.
 3. Run `bot.py`.
 4. In order to send a notification to a group defined in the database, add a
    JSON object with the keys `group` and `message` containing the relevant
    information to the queue. This can be done by using `notify.py`.

## License

This project is licensed under the MIT License, see LICENSE for details.

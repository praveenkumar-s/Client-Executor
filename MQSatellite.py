import sqlite3
import pika
import json
import sys
import socket
from datastore import file_db as DB
from uuid import uuid1
from datetime import datetime
import satlog

logger = satlog.get_logger("SATELLITE")
credentials = pika.PlainCredentials('praveen','abc@123')


def callback(ch, method, properties, body):
    id = str(uuid1())
    DB.execute_query_w("insert into QUEUE (ID , DATA , STATUS, CREATED_AT , NOTES)", (id , body , 'NEW', datetime.now() , ""))
    print(" [x] Received %r" % body)
    logger.debug("recived %r"%body)


if __name__ == "__main__":
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.1.7', 5672 ,'/',credentials))
    channel = connection.channel()
    channel.basic_consume(queue='helico',
                        auto_ack=True,
                        on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
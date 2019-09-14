#!/usr/bin/env python
import pika
import json
import model

credentials = pika.PlainCredentials('praveen','abc@123')
connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.1.13', 5672 ,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue='helico', durable=True)

prep_job = model.prepare_job("get_hostname", "hostname")

channel.basic_publish(exchange='',
                      routing_key='helico',
                      body=prep_job)
print(" [x] Sent Message")
connection.close()
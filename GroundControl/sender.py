#!/usr/bin/env python
import pika
import json

credentials = pika.PlainCredentials('praveen','abc@123')
connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.1.9', 5672 ,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue='helico', durable=True)

test_data ={
    "job_name":"CopyBuildPanamera",
    "execution_command":"robo copy do this",
    "Report_to":"channel",
    "report interval":""
}

channel.basic_publish(exchange='',
                      routing_key='helico',
                      body=json.dumps(test_data))
print(" [x] Sent Message")
connection.close()
#!/usr/bin/env python
import pika
import time

credentials = pika.PlainCredentials("praveen","abc@123")
connection = connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.1.9', 5672 ,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue='status', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='status', on_message_callback=callback)

channel.start_consuming()
import pika
import socket
import json

def acknowlege(queue,message,config):
    model={
        "action":"ack",
        "from":socket.gethostname(),
        "id":message["id"],
        "status":message["status"]
    }
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.1.9', 5672 ,'/',pika.PlainCredentials(config.RMQ.user , config.RMQ.password)))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(exchange='',
                      routing_key=queue,
                      body= json.dumps(model))    
    connection.close()    

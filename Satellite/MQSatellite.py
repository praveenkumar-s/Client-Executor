import pika
import json
import sys
from uuid import uuid4
from datetime import datetime
import Queries
import startup
import comm

config,DB,logger,credentials=None,None,None,None
connection = None



def callback(ch, method, properties, body):
    id = str(uuid4())
    body_json = json.loads(body)
    status=DB.execute_query_w(Queries.INSERT_MESSAGE, (id , body , 'NEW', datetime.now() , "",body_json['conmand']['time_out']))
    comm.acknowlege(config.RMQ.ack, {'id':id,"status":status}, config)
    logger.debug("recived %r"%body)


if __name__ == "__main__":
    
    config,DB,credentials,logger = startup.run()
    connection = pika.BlockingConnection(pika.ConnectionParameters(config.RMQ.host, config.RMQ.port ,'/',credentials))
    channel = connection.channel()
    channel.basic_consume(queue=config.RMQ.queue,
                        auto_ack=True,
                        on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
import pika
import json
import sys
from uuid import uuid1
from datetime import datetime
import Queries
import startup
import comm

config,DB,logger,credentials=None,None,None,None
connection = None



def callback(ch, method, properties, body):
    id = str(uuid1())
    status=DB.execute_query_w(Queries.INSERT_MESSAGE, (id , body , 'NEW', datetime.now() , ""))
    comm.acknowlege(config.RMQ.ack, {'id':id,"status":status}, config)
    logger.debug("recived %r"%body)


if __name__ == "__main__":
    
    config,DB,credentials,logger = startup.run()
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.2.1.9', 5672 ,'/',credentials))
    channel = connection.channel()
    channel.basic_consume(queue=config.RMQ.queue,
                        auto_ack=True,
                        on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
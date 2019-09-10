import json
from objectifier import Objectifier
import socket
from datastore import file_db
import pika
import satlog

def run():
    config = json.load(open('satellite_config.json'))
    config = Objectifier(config)
    config.RMQ.queue = socket.gethostname()
    DB = file_db(config.database)
    credentials = pika.PlainCredentials(config.RMQ.user,config.RMQ.password)
    logger = satlog.get_logger("SATELLITE")
    return config,DB,credentials,logger

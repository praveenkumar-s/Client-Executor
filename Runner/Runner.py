import json
import sqlite3
from subprocess import STDOUT, check_output
import subprocess
import sys
import time
import os
import satlog

logger = satlog.get_logger("RUNNER")
config = json.load(open('./runner/runnerConfig,json','r'))

GLOBAL_status={
    1:"NEW",
    2:"PICKED_UP",
    3:"COMPLETED",
    4:"TIME_OUT",
    5:"ERROR"
}

def get_records():
    data_set = None
    try:
        conn = sqlite3.connect(config['db_queue_path'])
        cursor = conn.cursor()
        cursor.execute("select * From queue where status = 'NEW' order by created_at limit 1;")
        data_set = cursor.fetchone()
    except:
        logger.error("Error Occured while getting records", stack_info=True)
    finally:
        conn.close()
        logger.info("found data {0}".format(str(data_set)))
        return data_set

def set_status(ref , status, notes = None):
    stat = None
    try:
        conn = sqlite3.connect(config['db_queue_path'])
        cursor = conn.cursor()
        cursor.execute("update queue set status = ?, notes = ? where ID =? ", ( GLOBAL_status[int(status)] , str(notes) , str(ref)))
        conn.commit()
        stat = True
    except:
        logger.error("error occured during updating status of {0} to {1}".format(ref , GLOBAL_status[int(status)]), stack_info=True)
        stat= False
    finally:
        conn.close()    
        logger.info("updated status of {0} to {1} successfully".format(ref , GLOBAL_status[int(status)]))    
        return stat

def process_records(data_set):
    ref_id= data_set[0]
    work = json.loads(data_set[1])
    time_out = data_set[6]
    set_status(ref_id , 2)
    stat = 1
    stack_trace = None
    output = None
    try:
        start_in = os.getcwd() if work["command"]["start_in"]=='.' else work["command"]["start_in"]
        logger.info("starting to execute command : "+str(work))
        output = check_output( work["command"]["cmd"], stderr=STDOUT, timeout=time_out, shell = True )
        logger.info("successfully executed the command!")
        stat = 3
    except subprocess.TimeoutExpired:
        stat = 4
        stack_trace = str(sys.exc_info())
        logger.error("command Failed during execution", stack_info=True)
    except:
        stat = 5
        stack_trace = str(sys.exc_info())
        logger.error("command Failed during execution", stack_info=True)
    finally:
        set_status(ref_id, stat, json.dumps({"output":str(output) , "stack_trace":stack_trace}))
    return output



while True:
    data_set = get_records()
    if(data_set is not None):
        print(process_records(data_set))
    time.sleep(10)
import json
import sqlite3
from subprocess import STDOUT, check_output

config = json.load(open('./runner/runnerConfig,json','r'))


def get_records():
    data_set = None
    try:
        conn = sqlite3.connect(config['db_queue_path'])
        cursor = conn.cursor()
        cursor.execute("select * From queue where status = 'NEW' order by created_at limit 1;")
        data_set = cursor.fetchone()
    except:
        #log 
        conn.close()
    finally:
        conn.close()
        return data_set

def process_records(data_set):
    ref_id= data_set[0]
    time_out = data_set[6]
    
    output = check_output(['python', 'scratchcode.py'], stderr=STDOUT, timeout=time_out)
    print(output)
    return output


import json

def prepare_job(job_name , command , start_in=".", run_as=None, command_timeout = 10000, report_to="status", report_interval =10 ):
    data_model = {
    "job_name":job_name,
    "conmand":{
        "cmd":command,
        "start_in":start_in,
        "run_as":run_as,
        "time_out":command_timeout
    },
    "report_to":report_to,
    "report interval":10
}
    return json.dumps(data_model)

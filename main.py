import string, uvicorn, socket, os, sys
from typing import Union, List
from dotenv import set_key
from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone, date
import json
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'], allow_credentials=True)
from memlog import MemoryLogRepository
from mongodb import MongoLogRepository

MONGO_HOST = None
MONGO_PORT = None
USE_MONGO = False
if 'USE_MONGO' in os.environ:
    USE_MONGO = os.environ['USE_MONGO']

if 'MONGO_HOST' in os.environ:
    MONGO_HOST = os.environ['MONGO_HOST']
if 'MONGO_PORT' in os.environ:
    MONGO_PORT = os.environ['MONGO_PORT']

logDB = MemoryLogRepository()
if USE_MONGO:
    logDB = MongoLogRepository(f"mongodb://{MONGO_HOST}:{MONGO_PORT}")

def custom_json_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif obj.toJson != None:
        return obj.toJson()
    raise TypeError (f"Type '{obj}' not serializable")


@app.get('/')
def welcome():
    return 'Welcome to SmartLog Server'

@app.post('/log/{appid}')
async def post_log(appid, batch: List[dict]):
    logDB.addBatchOfLogs(appid, batch)
    for item in batch:
        print(json.dumps(item, default=custom_json_serializer))
    return 'ok'

@app.post('/workflows/{appid}')
async def add_workflows(appid, batch: List[dict]):
    print('upload workflows:')
    print(batch)
    logDB.addBatchOfWorkflows(appid, batch)
    print('saved workflows:')
    print(json.dumps(logDB.getAppWorkflows(appid)))
    return 'ok'

@app.post('/issues/{appid}')
async def add_issues(appid, batch: List[dict] = Body()):
    logDB.addBatchOfIssues(appid, batch)
    print(json.dumps(logDB.getAppIssues(appid)))
    return 'ok'

@app.get('/log/{appid}')
def get_log(appid):
    return logDB.getAppLog(appid)

@app.delete('/log/{appid}')
def clear_app_log(appid):
    return logDB.clearAppLog(appid)

@app.get('/issues/{appid}')
def get_issues(appid):
    return logDB.getAppIssues(appid)
        
@app.get('/workflows/{appid}')
def get_workflows(appid):
    return logDB.getAppWorkflows(appid)

@app.get('/workflow/{appid}/{workflowid}')
def get_flows_by_workflow(appid: str, workflowid: str):
    return logDB.filterFlow(appid, workflowid)

@app.get('/workflow/{appid}/{workflowid}/{wiid}/logs')
def get_flow_logs(appid: str, workflowid: str, wiid: str):
    return logDB.getFlowLogs(appid, workflowid, wiid)


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


if __name__ == '__main__':
    uvicorn.run("main:app", host=extract_ip(), port=24505)
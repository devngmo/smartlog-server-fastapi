import string, uvicorn, socket
from typing import Union, List
from dotenv import set_key
from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import json
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'], allow_credentials=True)
from memlog import MemoryLogRepository

mlIns = MemoryLogRepository()

@app.get('/')
def welcome():
    return 'Welcome to SmartLog Server'

@app.post('/log/{appid}')
async def post_log(appid, batch: List[dict]):
    mlIns.addBatchOfLogs(appid, batch)
    return 'ok'

@app.post('/workflows/{appid}')
async def add_workflows(appid, batch: List[dict]):
    print('upload workflows:')
    print(batch)
    mlIns.addBatchOfWorkflows(appid, batch)
    print('saved workflows:')
    print(json.dumps(mlIns.getAppWorkflows(appid)))
    return 'ok'

@app.post('/issues/{appid}')
async def add_issues(appid, batch: List[dict] = Body()):
    mlIns.addBatchOfIssues(appid, batch)
    print(json.dumps(mlIns.getAppIssues(appid)))
    return 'ok'

@app.get('/log/{appid}')
def get_log(appid):
    return mlIns.getAppLog(appid)

@app.delete('/log/{appid}')
def clear_app_log(appid):
    return mlIns.clearAppLog(appid)

@app.get('/issues/{appid}')
def get_issues(appid):
    return mlIns.getAppIssues(appid)
        
@app.get('/workflows/{appid}')
def get_workflows(appid):
    return mlIns.getAppWorkflows(appid)

@app.get('/workflow/{appid}/{workflowid}')
def get_flows_by_workflow(appid: str, workflowid: str):
    return mlIns.filterFlow(appid, workflowid)

@app.get('/workflow/{appid}/{workflowid}/{wiid}/logs')
def get_flow_logs(appid: str, workflowid: str, wiid: str):
    return mlIns.getFlowLogs(appid, workflowid, wiid)


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
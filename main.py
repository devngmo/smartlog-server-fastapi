import string
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
        
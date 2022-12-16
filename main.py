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
mlIns.addAll('smartlog', [{'type': 'info', 'msg': 'started'}])

@app.get('/')
def welcome():
    return 'Welcome to SmartLog Server'

@app.post('/log/{appid}')
async def post_log(appid, batch: List[dict] = Body()):
    print('add %d entries' % len(batch))
    assert isinstance(batch, list)
    mlIns.addAll(appid, batch)
    return 'ok'


@app.get('/log/{appid}')
def get_log(appid):
    return mlIns.getAppLog(appid)
        
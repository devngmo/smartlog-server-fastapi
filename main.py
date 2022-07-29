import string
from typing import Union
from dotenv import set_key
from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import json
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*', 'http://localhost:8000', 'http://localhost:3000'], allow_methods=['*'], allow_headers=['*'], allow_credentials=True)
from memlog import MemoryLogRepository

mlIns = MemoryLogRepository()

@app.get('/')
def welcome():
    return 'Welcome to SmartLog Server'

@app.post('/log/{appid}')
async def post_log(appid, request: Request):
    batch = await request.json()
    mlIns.addAll(appid, batch)
    return 'ok'


@app.get('/log/{appid}')
def get_log(appid):
    return mlIns.getAppLog(appid)
        
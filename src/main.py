from fastapi import FastAPI, Request
from pydantic import BaseModel
import api.endpoint.v1.user
import api.endpoint.v1.account
import api.endpoint.v1.session
from api.object.sqlite import SQLiteSession
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
security = HTTPBearer()
    

@app.post('/api/v1/user/session/')
async def v1_post_user_session(request:Request): 
    return await api.endpoint.v1.session.create(request)

# list of API endpoints and their handlers
@app.get('/api/v1/user/')
async def v1_get_user(request:Request): 
    return await api.endpoint.v1.user.get(request)

# list of API endpoints and their handlers
@app.get('/api/v1/account/list/')
async def v1_get_account_list(request:Request): 
    return await api.endpoint.v1.account.list(request)

# list transfers for this account
@app.get('/api/v1/account/{id}/transfers/')
async def v1_get_account_list(request:Request, id:int): 
    return await api.endpoint.v1.account.list_transactions(request, id)


from fastapi import FastAPI, Request
from pydantic import BaseModel
import api.endpoint.v1.user
import api.endpoint.v1.account

app = FastAPI()


# list of API endpoints and their handlers
@app.get('/api/v1/user/')
async def v1_get_user(request:Request): 
    return await api.endpoint.v1.user.get(request)

# list of API endpoints and their handlers
@app.get('/api/v1/account/list/')
async def v1_get_account_list(request:Request): 
    return await api.endpoint.v1.account.list(request)

@app.get('/api/v1/account/{account_id}/')
async def v1_get_account_list(request:Request, account_id:int): 
    return await api.endpoint.v1.account.list(request, account_id)


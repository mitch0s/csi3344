from fastapi import FastAPI, Request
from pydantic import BaseModel
import api.endpoint.v1.user

app = FastAPI()


# list of API endpoints and their handlers
@app.get('/api/v1/user/')
async def v1_get_user(request:Request): 
    return await api.endpoint.v1.user.get(request)

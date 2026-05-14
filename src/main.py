import asyncio
from fastapi import FastAPI, Request
from fastapi import WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
import api.endpoint.v1.user
import api.endpoint.v1.account
import api.endpoint.v1.session
from api.util.dateutil import timestamp_now_utc
import logging
from taskgroup import TaskGroup

logger = logging.getLogger()

active_websocket_clients = set()

@asynccontextmanager
async def lifespan(app:FastAPI):
    # startup stuff
    logger.info('Starting up...')
    yield
    logger.info('Disconnecting websocket clients...')
    ws_client:WebSocket
    for ws_client in active_websocket_clients:
        ws_client.close(1000)


app = FastAPI(lifespan=lifespan)    

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


async def broadcast_new_user_count():
    message = {'type': 'live_user_count', 'timestamp': timestamp_now_utc(), 'data': [{'value': len(active_websocket_clients)}]}
    ws_client:WebSocket
    for ws_client in active_websocket_clients:
        try: await ws_client.send_json(message)
        except: pass

@app.websocket('/ws')
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()
    active_websocket_clients.add(websocket)
    logger.info('Websocket connected.')
    await broadcast_new_user_count()

    async def ws_write_task(websocket:WebSocket):
        counter = 0
        while True:
            await asyncio.sleep(1)
            await websocket.send_json({'type': 'new_message', 'timestamp': timestamp_now_utc(), 'data': [{'username': 'mitch0s', 'content': f'Hello, world! [{counter}]'}]})
            counter += 1

    async def ws_read_task(websocket:WebSocket):
        while True:
            message = await websocket.receive_text()
            logger.info(f'WS_MESSAGE: {message}')

    try:
        async with TaskGroup() as tg:
            tg.create_task(ws_write_task(websocket))
            tg.create_task(ws_read_task(websocket))
    except Exception as error:
        active_websocket_clients.remove(websocket)
        await broadcast_new_user_count()
        logger.info(error)

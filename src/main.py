import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import api.endpoint.v1.user as user_api
import api.endpoint.v1.account as account_api
import api.endpoint.v1.session as session_api

from api.util.dateutil import timestamp_now_utc
from taskgroup import TaskGroup

logger = logging.getLogger(__name__)

# ----------------------------
# App setup
# ----------------------------

api_router = APIRouter(prefix="/api/v1")
active_websocket_clients: set[WebSocket] = set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")

    yield

    logger.info("Shutting down WebSocket clients...")

    for ws in list(active_websocket_clients):
        try:
            await ws.close(code=1000)
        except Exception:
            pass

    active_websocket_clients.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/{file}/")
async def get_file(request:Request, file:str):
    if '.' not in file:
        file += '.html'
    
    return FileResponse(f'src/static/{file}')


# ----------------------------
# API routes
# ----------------------------

@api_router.post("/user/session/")
async def create_session(request: Request):
    return await session_api.create(request)


@api_router.get("/user/")
async def get_user(request: Request):
    return await user_api.get(request)


@api_router.get("/account/list/")
async def list_accounts(request: Request):
    return await account_api.list(request)


@api_router.get("/account/{account_id}/transfers/")
async def list_account_transfers(request: Request, account_id: int):
    return await account_api.list_transactions(request, account_id)


app.include_router(api_router)


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

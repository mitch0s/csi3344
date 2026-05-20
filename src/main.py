import asyncio
import logging
import random
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import FileResponse, RedirectResponse

from api.websocket.websocket import SessionWebSocket, active_websocket_sessions
import api.endpoint.v1.user as user_api
import api.endpoint.v1.account as account_api
import api.endpoint.v1.session as session_api
import api.endpoint.v1.transfer as transfer_api

from api.object.sqlite.sqlite_fee_manager import SQLiteFeeManager
from api.worker import *

from api.util.dateutil import timestamp_utc
from taskgroup import TaskGroup

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("Starting up...")

    # start up transaction processor
    asyncio.create_task(g_transaction_processor.run_forever())

    yield  # yields back to async manager.
           # all code below this runs when async manager returns back (on server close)

    logger.info("Shutting down WebSocket clients...")

    for ws in list(active_websocket_sessions):
        try:
            await ws.close(code=1000)
        except Exception:
            pass

    active_websocket_sessions.clear()


app = FastAPI(lifespan=lifespan)


# static content retrieval.
@app.get("/")
async def redirect():
    return RedirectResponse('/home')

@app.get("/{file}")
async def get_file(request:Request, file:str):
    if '.' not in file:
        file += '.html'
    return FileResponse(f'src/static/{file}')

@app.get("/{entity}/{id}")
async def get_file(request:Request, entity:str, id:int):
    if '.' not in entity:
        entity += '.html'
    return FileResponse(f'src/static/{entity}')


@app.post("/api/v1/user/session/")
async def create_session(request: Request):
    return await session_api.create(request)

@app.get("/api/v1/user/")
async def get_user(request: Request):
    return await user_api.get(request)

@app.get("/api/v1/account/list/")
async def list_accounts(request: Request):
    return await account_api.list(request)

@app.get("/api/v1/account/{account_id}/transfers/")
async def list_account_transfers(request:Request, account_id: int):
    return await account_api.list_transactions(request, account_id)

@app.post("/api/v1/transfer/")
async def list_account_transfers(request:Request):
    return await transfer_api.create(request)


# websocket stuff
async def broadcast_new_user_count():
    message = {'type': 'live_user_count', 'timestamp': timestamp_utc(), 'data': [{'value': len(active_websocket_sessions)}]}
    ws_client:SessionWebSocket
    for ws_client in active_websocket_sessions:
        try: await ws_client.send_json(message)
        except: pass

async def account_created_data(id:int=None):
    rand = random.randint(0, 10)
    id = id or rand
    rand_balance = random.randint(0, 99999)
    return {'id': id, 'name': f'Account #{rand}', 'balance_cents': rand_balance}

async def account_updated_data(id:int):
    rand = random.randint(0, 10)
    rand_balance = random.randint(0, 99999)
    return {'id': id, 'name': f'Account #{rand}', 'balance_cents': rand_balance}
    

@app.websocket('/ws')
async def websocket_endpoint(og_websocket:WebSocket):
    websocket:SessionWebSocket = SessionWebSocket(og_websocket)
    await websocket.accept()
    active_websocket_sessions.append(websocket)
    logger.info('Websocket connected.')
    await broadcast_new_user_count()

    async def ws_write_task(websocket:SessionWebSocket):
        if websocket.user:
            while True:
                await asyncio.sleep(1)
                pass

    async def ws_read_task(websocket:SessionWebSocket):
        while True:
            message:dict = await websocket.receive_json()
            match message.get('type'):
                case 'client_auth':
                    token = message.get('data', [{}])[0].get('session_token')
                    if token:
                        websocket.set_session(token)    
                case 'transfer_fee':
                    if websocket.user:
                        print('valid user!')
                        transfer_amount_cents = message.get('data', {}).get('transfer_amount_cents')
                        fee_amount_cents = SQLiteFeeManager().calculate_fee_charge_cents(transfer_amount_cents)
                        data = { 'transfer_amount_cents': transfer_amount_cents, 'fee_amount_cents': fee_amount_cents }
                        await websocket.emit('transfer_fee', data)
                        
    try:
        async with TaskGroup() as tg:
            tg.create_task(ws_write_task(websocket))
            tg.create_task(ws_read_task(websocket))
    except Exception as error:
        # traceback.print_exc()
        active_websocket_sessions.remove(websocket)
        await broadcast_new_user_count()
        logger.info(error)
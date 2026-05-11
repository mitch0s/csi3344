from fastapi import Request
from fastapi.responses import JSONResponse
from api.object.sqlite.SQLiteUser import SQLiteUser
from api.object.sqlite.SQLiteSession import SQLiteSession
from api.object.sqlite.SQLiteAccount import SQLiteAccount
from api.object.base.errors import *
from api.util.dateutil import timestamp_now_utc

async def list(request:Request):
    try: 
        data:dict = await request.json()
        data:dict = await request.json()
        if 'session_token' not in data:
            return JSONResponse({'status': 'error', 'timestamp': timestamp_now_utc(), 'reason': 'no "session_token" field was supplied in request body.'}, status_code=400)
        
        session:SQLiteSession = SQLiteSession(token=data.get('session_token'))
        user:SQLiteUser = session.user
        
        account_data = []
        for account in user.accounts:
            account_data.append(account.data)

        # user = SQLiteUser(id=1)
        return JSONResponse({'status': 'success', 'timestamp': timestamp_now_utc(), 'data': account_data})
    
    except SessionNotFound   : return JSONResponse({'status': 'error', 'timestamp': timestamp_now_utc(), 'reason': 'invalid session token supplied.'}, status_code=404)
    except UserNotFoundError : return JSONResponse({'status': 'error', 'timestamp': timestamp_now_utc(), 'reason': 'no user with the specified id exists.'}, status_code=404)


async def transactions(request:Request, id:int):
    try: 
        data:dict = await request.json()
        data:dict = await request.json()
        if 'session_token' not in data:
            return JSONResponse({'status': 'error', 'timestamp': timestamp_now_utc(), 'reason': 'no "session_token" field was supplied in request body.'}, status_code=400)
        
        session:SQLiteSession = SQLiteSession(token=data.get('session_token'))
        user:SQLiteUser = session.user
        account:SQLiteAccount = None
        for t_account in user.accounts:
            if t_account.id == id:
                account = t_account
                break
        if account is None : raise AccountNotFoundError()

        transaction_data = []
        for transfer in account.transfers:
            transaction_data.append(transfer.data)

        # user = SQLiteUser(id=1)
        return JSONResponse({'status': 'success', 'timestamp': timestamp_now_utc(), 'data': transaction_data})
    
    except SessionNotFound      : return JSONResponse({'status': 'error', 'timestamp': timestamp_now_utc(), 'reason': 'invalid session token supplied.'}, status_code=404)
    except UserNotFoundError    : return JSONResponse({'status': 'error', 'timestamp': timestamp_now_utc(), 'reason': 'no user with the specified id exists.'}, status_code=404)
    except AccountNotFoundError : return JSONResponse({'status': 'error', 'timestamp': timestamp_now_utc(), 'reason': 'no account with the specified id exists.'}, status_code=404)
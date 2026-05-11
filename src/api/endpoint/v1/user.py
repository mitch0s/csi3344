from fastapi import Request
from fastapi.responses import JSONResponse
from api.object.sqlite.SQLiteUser import SQLiteUser
from api.object.sqlite.SQLiteSession import SQLiteSession
from api.object.base.errors import *
from api.util.dateutil import timestamp_now_utc

async def get(request:Request):
    try: 
        data:dict = await request.json()
        if 'session_token' not in data:
            return JSONResponse({'status': 'error', 'reason': 'no "session_token" field was supplied in request body.'}, status_code=400)
        
        session:SQLiteSession = SQLiteSession(token=data.get('session_token'))
        user:SQLiteUser = session.user

        
        # user = SQLiteUser(id=1)
        return JSONResponse({'status': 'success', 'ts': timestamp_now_utc(), 'data': user.data})
    
    except SessionNotFound   : return JSONResponse({'status': 'error', 'ts': timestamp_now_utc(), 'reason': 'invalid session token supplied.'}, status_code=404)
    except UserNotFoundError : return JSONResponse({'status': 'error', 'ts': timestamp_now_utc(), 'reason': 'no user with the specified id exists.'}, status_code=404)
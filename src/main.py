import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api.object.sqlite.SQLiteUser import SQLiteUser
from api.util.dateutil import timestamp_now_utc
app = FastAPI()

# @app.exception_handler()
# async def handle_exception(500):
#     return JSONResponse({'status': 'error', 'reason': traceback.format_exc(exc)})

@app.get('/api/v1/user/{user_id}/')
async def v1_get_user(user_id:int):
    user = SQLiteUser(id=1)
    print(user.accounts[0])
    return JSONResponse({'user_id': user_id, 'ts': timestamp_now_utc()})


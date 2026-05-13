from fastapi import Request
from api.object.sqlite import SQLiteSession, SQLiteUser
from api.object.base.errors import *
from api.response.json_response import *
from api.util.parse_headers import parse_authorization_header


async def get(request:Request):
    try: 
        session_token = parse_authorization_header(request.headers)
        session:SQLiteSession = SQLiteSession(session_token)
        session.validate_expiry()
        user:SQLiteUser = session.user
        
        # user = SQLiteUser(id=1)
        return SuccessResponse(content=user.data)
    
    except InvalidSessionError  : return NotFoundResponse('invalid session token.')
    except UserNotFoundError    : return NotFoundResponse('invalid session token.')
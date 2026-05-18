from fastapi import Request
from api.object.sqlite.sqlite_session import SQLiteSession
from api.object.sqlite.sqlite_user import SQLiteUser
from api.object.base.errors import *
from api.response.json_response import *
from json import JSONDecodeError
from api.util.hashing import hash_password

async def create(request: Request):
    try:
        data: dict = await request.json()
        # ensure that required fields are in request body (json)
        if 'email_address' not in data or 'password' not in data:
            raise RequestValidationError("'email_address' and 'password' fields are required in request body.")

        email = data.get('email_address')
        password = data.get('password')

        user = SQLiteUser.get_by_email_address(email)
        if not user:
            raise UserNotFoundError()

        user.validate_password(password)
        
        session = SQLiteSession.create(user=user)

        return SuccessResponse(content={'session_token': session.token})

    except UserNotFoundError           : return NotFoundResponse('invalid credentials.')
    except InvalidPasswordError        : return NotFoundResponse('invalid credentials.')
    except JSONDecodeError as e        : return BadRequestResponse('invalid request body.')
    except RequestValidationError as e : return BadRequestResponse(str(e))
from fastapi import Request
from api.object.sqlite.sqlite_session import SQLiteSession
from api.object.sqlite.sqlite_user import SQLiteUser
from api.object.sqlite.sqlite_account import SQLiteAccount
from api.object.base.errors import *
from api.response.json_response import *
from api.util.parse_headers import parse_authorization_header

async def list(request:Request):
    try: 
        session_token = parse_authorization_header(request.headers)
        session:SQLiteSession = SQLiteSession(session_token)
        session.validate_expiry()  # raises SessionExpiredError
        
        user:SQLiteUser = session.user
        
        account_data = []
        for account in user.accounts:
            account_data.append(account.data)

        return SuccessResponse(content=account_data)
    
    except InvalidSessionError         : return NotFoundResponse('invalid session token.')
    except UserNotFoundError           : return NotFoundResponse('invalid session token.')  # also return invalid session if user doesn't exist
    except RequestValidationError as e : return BadRequestResponse(str(e))

async def create(request:Request):
    try: 
        session_token = parse_authorization_header(request.headers)
        session:SQLiteSession = SQLiteSession(session_token)
        session.validate_expiry()  # raises SessionExpiredError
        
        user:SQLiteUser = session.user
        
        account_data = []
        for account in user.accounts:
            account_data.append(account.data)

        return SuccessResponse(content=account_data)
    
    except InvalidSessionError         : return NotFoundResponse('invalid session token.')
    except UserNotFoundError           : return NotFoundResponse('invalid session token.')  # also return invalid session if user doesn't exist
    except RequestValidationError as e : return BadRequestResponse(str(e))


async def list_transactions(request:Request, id:int):
    try: 
        session_token = parse_authorization_header(request.headers)
        session:SQLiteSession = SQLiteSession(session_token)
        session.validate_expiry()  # raises SessionExpiredError
        user:SQLiteUser = session.user
        account:SQLiteAccount = None
        for t_account in user.accounts:
            if t_account.id == id:
                account = t_account
                break
        if account is None : raise AccountNotFoundError()

        transaction_data = []
        for transfer in account.transfers:
            data = transfer.data
            data['amount_cents'] = transfer.amount_by_account_id(id=account.id)
            transaction_data.append(data)

        # user = SQLiteUser(id=1)
        return SuccessResponse(transaction_data)
    
    except InvalidSessionError         : return NotFoundResponse('invalid session token.')
    except UserNotFoundError           : return NotFoundResponse('invalid session token.')
    except AccountNotFoundError        : return NotFoundResponse('account specified does not exist.')
    except RequestValidationError as e : return BadRequestResponse(str(e))
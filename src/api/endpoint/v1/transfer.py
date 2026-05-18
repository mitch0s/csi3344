from fastapi import Request
from api.object.sqlite.sqlite_session import SQLiteSession
from api.object.sqlite.sqlite_user import SQLiteUser
from api.object.sqlite.sqlite_account import SQLiteAccount
from api.object.sqlite.sqlite_transfer import SQLiteTransfer
from api.object.sqlite.sqlite_fee_manager import SQLiteFeeManager
from api.object.base.errors import *
from api.response.json_response import *
from api.util.parse_headers import parse_authorization_header

# post
async def create(request:Request):
    try: 
        session_token = parse_authorization_header(request.headers)
        session:SQLiteSession = SQLiteSession(session_token)
        session.validate_expiry()  # raises SessionExpiredError

        body:dict = await request.json()
        required_body_items = ['user_account_id', 'recipient_account_id', 'transfer_amount_cents']
        for item in required_body_items:
            if item not in body : raise BadRequestResponse(f'This request is missing one or more required fields: {required_body_items}')
            value = body.get(item)
            if type(value) is not int : raise RequestValidationError(f'{item} field must be positive integer')
            if value <= 0             : raise RequestValidationError(f'{item} field must be positive integer')

        user:SQLiteUser = session.user
        user_account:SQLiteAccount = user.get_account(body.get('user_account_id'))

        recipient_account_id = body.get('recipient_account_id')
        try: recipient_account = SQLiteAccount(recipient_account_id)
        except AccountNotFoundError: raise AccountNotFoundError('Recipient account could not be found')

        transfer_amount_cents = body.get('transfer_amount_cents')
        fee_amount_cents      = SQLiteFeeManager().calculate_fee_charge_cents(amount_cents=transfer_amount_cents)

        total_amount_cents = transfer_amount_cents + fee_amount_cents
        if total_amount_cents > user_account.balance_cents:
            raise RequestValidationError('insufficient funds in user balance to process request.')

        transfer = SQLiteTransfer.create(sender=user_account, receiver=recipient_account, amount_cents=transfer_amount_cents, fee_cents=fee_amount_cents)

        return SuccessResponse(content=[{'transfer': transfer.data}])
    
    except InvalidSessionError         : return NotFoundResponse('invalid session token.')
    except UserNotFoundError           : return NotFoundResponse('invalid session token.')  # also return invalid session if user doesn't exist
    except AccountNotFoundError   as e : return NotFoundResponse(str(e))
    except RequestValidationError as e : return BadRequestResponse(str(e))


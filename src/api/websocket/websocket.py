from fastapi import WebSocket
from api.object.base import BaseSession, BaseUser, BaseAccount, BaseTransfer
from api.object.sqlite.sqlite_session import SQLiteSession 
from api.util.dateutil import timestamp_utc

class SessionWebSocket(WebSocket):
    """
    subclass of fastapi.WebSocket. Used to track session information.
    """
    def __init__(self, ws:WebSocket):
        self.ws = ws
        self._session:BaseSession = None
        super().__init__(ws.scope, ws._receive, ws._send)

    @property
    def user(self) -> BaseUser:
        if self._session:
            return self._session.user
        return None

    def set_session(self, token:str) -> None:
        self._session = SQLiteSession(token)

    async def emit(self, event:str, data:object) -> None:
        if type(event) is not str : raise Exception('Event type argument must be string type')
        if type(data) not in [dict, list, int, float, str]  : raise Exception('Event data argument must be string type')

        if type(data) == list: data = data
        elif type(data) == dict: data = [data]
        else: data = [{'value': data}]

        _message = {'type': event, 'timestamp': timestamp_utc(), 'data': data}
        await self.send_json(_message)

    async def send_account_created_message(self, account:BaseAccount):
        self._session.validate_expiry()

        data = {
            'id': account.id,
            'name': account.name,
            'balance_cents': account.balance_cents
        }
        self.send(event='account_created', data=data)

    async def send_transfer_created_message(self, transfer:BaseTransfer):
        self._session.validate_expiry()
        data = {
            'id': transfer.id,
            'status': transfer.status,
            'created_utc': transfer.created_utc,
            'user_note': transfer.user_note,
            'amount_cents': transfer.amount_cents,
            'items': []
        }
        for transfer_item in transfer.items:
            data['items'].append(transfer_item.data)
        await self.emit(event='transfer_created', data=data)

    async def send_transfer_updated_message(self, transfer:BaseTransfer):
        self._session.validate_expiry()
        data = {
            'id': transfer.id,
            'status': transfer.status,
            'created_utc': transfer.created_utc,
            'user_note': transfer.user_note,
            'amount_cents': transfer.amount_cents,
            'items': []
        }
        for transfer_item in transfer.items:
            data['items'].append(transfer_item.data)
        await self.emit(event='transfer_updated', data=data)

    def close(self, code=1000, reason=None):
        active_websocket_sessions.remove(self)
        return super().close(code, reason)
    
# track active websocket sessions
active_websocket_sessions:list[SessionWebSocket] = []
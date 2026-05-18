from fastapi import WebSocket
from api.object.base import BaseSession, BaseUser, BaseAccount
from api.object.sqlite import SQLiteSession, SQLiteUser
from api.util.dateutil import timestamp_now_utc

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

        _message = {'type': event, 'timestamp': timestamp_now_utc(), 'data': data}
        await self.send_json(_message)

    def send_account_created_message(self, account:BaseAccount):
        self._session.validate_expiry()

        data = {
            'id': account.id,
            'name': account.name,
            'balance_cents': account.balance_cents
        }
        self.send(event='account_created', data=data)

    def close(self, code=1000, reason=None):
        active_websocket_sessions.remove(self)
        return super().close(code, reason)


    
# track active websocket sessions
active_websocket_sessions:list[SessionWebSocket] = []
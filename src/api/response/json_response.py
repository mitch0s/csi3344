from fastapi.responses import JSONResponse
from api.util.dateutil import timestamp_now_utc


class SuccessResponse(JSONResponse):
    def __init__(self, content, headers=None, media_type=None, background=None):
        # wrap content in success status message with timestamp. All data under 'data' field.
        content = {'status': 'success', 'timestamp': timestamp_now_utc(), 'data': content}
        super().__init__(content, 200, headers, media_type, background)

class BadRequestResponse(JSONResponse):
    def __init__(self, message:str, headers=None, media_type=None, background=None):
        # wrap content in success status message with timestamp. All data under 'data' field.
        content = {'status': 'error', 'reason': message, 'timestamp': timestamp_now_utc(), 'data': None}
        super().__init__(content, 400, headers, media_type, background)

class NotFoundResponse(JSONResponse):
    def __init__(self, message:str, headers=None, media_type=None, background=None):
        # wrap content in success status message with timestamp. All data under 'data' field.
        content = {'status': 'error', 'reason': message, 'timestamp': timestamp_now_utc(), 'data': None}
        super().__init__(content, 404, headers, media_type, background)
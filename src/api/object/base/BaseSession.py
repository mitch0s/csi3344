from .BaseUser import BaseUser


class BaseSession:
    def __init__(self, token:str):
        self.token = token
        self.user:BaseUser
        self.created_utc:str
        self.expiry_utc:str
        self._load()

    def _load(self):
        raise NotImplementedError()
    

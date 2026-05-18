from .BaseTransfer import BaseTransfer



class BaseAccount:
    def __init__(self, id:int):
        # public and mostly static attributes.
        self.id = id
        self.name:str
        self.created_utc:str
        self.status:str
        self.balance_cents:int = 0
        self.available_balance_cents:int = 0
        # call 'private' load method
        self._load()

    def _load(self):
        raise NotImplementedError()
    
    @property
    def transfers(self) -> list[BaseTransfer]:
        raise NotImplementedError()
    
    @property
    def data(self) -> dict:
        raise NotImplementedError()
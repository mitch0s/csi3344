from .BaseTransaction import BaseTransaction


class BaseAccount:
    def __init__(self, id:int):
        # public and mostly static attributes.
        self.id = id
        self.name:str
        self.created_utc:str
        self.status:str
        # call 'private' load method
        self._load()

    def _load(self):
        raise NotImplementedError()
    
    @property
    def transactions(self) -> list[BaseTransaction]:
        raise NotImplementedError()
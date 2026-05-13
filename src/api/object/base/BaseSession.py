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
    
    def validate_expiry() -> None:
        """
        raise SessionExpiredError if current session is expired
        :returns: Nothing. No exception is raised if session is valid.
        """
        raise NotImplementedError()

    @property
    def data(self) -> dict:
        raise NotImplementedError()
    
    @staticmethod
    def create(user:BaseUser):
        raise NotImplementedError()
    

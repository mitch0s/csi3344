from .BaseAccount import BaseAccount

class BaseUser:
    def __init__(self, id:int):
        # list of basic top-level User attributes
        self.id:int = id
        self.first_name:str
        self.last_name:str
        self.email_address:str
        self.password_hash:str
        self.created_utc:str
        self.status:str
        # call 'private' load method (to be implemented per-subclass of BaseUser)
        self._load()

    def _load(self):
        """
        Loader method used to fetch actual User info by ID.
        """
        raise NotImplementedError()
    
    @staticmethod
    def get_by_email_address(email_address:str):
        """
        Helper method that returns user instance by email address.
        :email_address: unique email address of user account.
        :returns: BaseUser (or subclass) instance.
        """
        raise NotImplementedError()

    @property
    def accounts(self) -> list[BaseAccount]:
        """
        Property method that returns a list of BaseAccounts to caller. To be implemented by subclass.
        """
        raise NotImplementedError()

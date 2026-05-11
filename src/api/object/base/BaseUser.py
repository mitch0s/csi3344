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
    
    @property
    def data(self) -> dict:
        raise NotImplementedError()

    def _load(self):
        """
        Loader method used to fetch actual User info by ID.
        """
        raise NotImplementedError()
    
    def validate_password(password:str) -> bool:
        """
        Check a password input string against the stored password hash.
        :password: raw string input from user to be compared against stored password hash.
        :returns: boolean value representing password match
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
    
    @staticmethod 
    def create(first_name:str, last_name:str, email_address:str, password:str):
        """
        Method used to create new user account.
        :first_name: First name of user who owns the account.
        :last_name: Last name of user who owns the account.
        :email_address: Email address of the person who owns the account.
        :password: Raw password string used to sign into the account.
        :returns: BaseUser or subclass.
        """
        raise NotImplementedError()

    @property
    def accounts(self) -> list[BaseAccount]:
        """
        Property method that returns a list of BaseAccounts to caller. To be implemented by subclass.
        :returns: list of BaseAccount or subclass instances.
        """
        raise NotImplementedError()

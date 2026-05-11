
class BaseTransfer:
    def __init__(self, id:int):
        self.id:int = id
        self.user_note:str
        self.total_cents:int
        self.created_utc:str
        self.status:str
        self._load()

    def _load(self):
        """
        Loader method used to fetch actual User info by ID.
        """
        raise NotImplementedError()
    
    @property
    def items() -> list:
        """
        Property method that fetches and returns a list of BaseTransferItems (transaction line items).
        :returns: list[BaseTransferItem]
        """
        raise NotImplementedError()
    
    @property
    def amount_cents(self):
        """
        Property method that returns the total transaction amount (including fees)
        """
        raise NotImplementedError()


from .BaseAccount import BaseAccount

class BaseTransferItem:
    def __init__(self):
        self.creditor:BaseAccount
        self.debitor:BaseAccount
        self.amount_cents:int

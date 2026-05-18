from .BaseAccount import BaseAccount

class BaseTransferItem:
    def __init__(self):
        self.id:int
        self.creditor:BaseAccount
        self.debtor:BaseAccount
        self.amount_cents:int
        self.type:str

    @property
    def data(self) -> dict:
        return {
            'id': self.id,
            # 'cr_account_id': self.creditor.id,
            # 'dr_account_id': self.debtor.id,
            'amount_cents': self.amount_cents,
            'type': self.type
        }
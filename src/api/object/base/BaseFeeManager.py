from dataclasses import dataclass
from api.object.base.errors import FeeNotFoundError
import math

@dataclass
class FeeTier:
    def __init__(self, id:int, range_min_cents:int, range_max_cents:int, fee_percentage:float, transfer_cap_cents:int, description:str):
        self.id:int = id
        self.range_min_cents:int = range_min_cents
        self.range_max_cents:int = range_max_cents
        self.fee_percentage:float = fee_percentage
        self.transfer_cap_cents:int = transfer_cap_cents
        self.description:str = description

    @property
    def data(self) -> dict:
        return self.__dict__.copy()



class BaseFeeManager:
    def __init__(self):
        self._load()  # call _load method (to be implemented by subclass)
        
    def _load(self):
        """
        Loader method called for all subclasses of BaseFeeManager. Not really used,
        remains a part of class constructor for future unknown-unknowns --> really f*****g hate unknown unknowns.
        """
        raise NotImplementedError()
    
    @property
    def tiers(self) -> list[FeeTier]:
        """
        Query database and return list of FeeTier instances.
        This method raises NotImplementedError unless overridden by a subclass definition.
        """
        raise NotImplementedError()


    def get_transfer_amount_tier(self, amount_cents:int) -> FeeTier:
        """
        Iterate over all fee tiers and determine
        """
        for tier in self.tiers:
            # start/stop range values are inclusive at both ends!!!!!!
            if tier.range_min_cents <= amount_cents <= tier.range_max_cents:
                return tier
        raise FeeNotFoundError(f'could not find a fee tier for amount {amount_cents}')
    

    def calculate_fee_charge_cents(self, amount_cents:int) -> int:
        """
        Fetch fee tier for transfer amount, calculate fee. Sub-cent value is rounded upwards to nearest cent.
        This biases towards the bank, and prevents fee undercalculation.
        """
        fee_tier:FeeTier = self.get_transfer_amount_tier(amount_cents=amount_cents)
        fee_amount_cents = amount_cents * fee_tier.fee_percentage
        fee_amount_cents = int(math.ceil(fee_amount_cents))  # round sub-cent amounts up to nearest cent. bias is for bank, against customer.
        fee_amount_cents = min(fee_amount_cents, fee_tier.transfer_cap_cents)  # use lowest fee amount (calculated fee vs. tier cap)
        
        return fee_amount_cents


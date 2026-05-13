import pytest
from api.object.sqlite import SQLiteFeeManager, FeeTier
from api.object.base.errors import FeeNotFoundError


FREE_TIER         = {'id': 0, 'range_min_cents': 0,        'range_max_cents': 200000,    'fee_percentage': 1.0,   'transfer_cap_cents': 0,     'description': 'Free tier'}
ENTRY_TIER        = {'id': 1, 'range_min_cents': 200001,   'range_max_cents': 1000000,   'fee_percentage': 0.25,  'transfer_cap_cents': 2000,  'description': 'Entry tier'}
MID_TIER          = {'id': 2, 'range_min_cents': 1000001,  'range_max_cents': 2000000,   'fee_percentage': 0.2,   'transfer_cap_cents': 2500,  'description': 'Mid tier'}
UPPER_MIDDLE_TIER = {'id': 3, 'range_min_cents': 2000001,  'range_max_cents': 5000000,   'fee_percentage': 0.125, 'transfer_cap_cents': 4000,  'description': 'Upper-mid tier'}
HIGH_TIER         = {'id': 4, 'range_min_cents': 5000001,  'range_max_cents': 10000000,  'fee_percentage': 0.08,  'transfer_cap_cents': 6000,  'description': 'High tier'}
TOP_TIER          = {'id': 5, 'range_min_cents': 10000001, 'range_max_cents': 999999999, 'fee_percentage': 0.06,  'transfer_cap_cents': 20000, 'description': 'Top tier'}


@pytest.mark.parametrize("AMOUNT_CENTS, EXPECTED_TIER, EXPECTED_EXCEPTION", [
    (-1,         FREE_TIER,         FeeNotFoundError),  # below free tier lower bound
    (0,          FREE_TIER,         None), # at free tier lower bound
    (1,          FREE_TIER,         None), # above free tier lower bound
    (199999,     FREE_TIER,         None), # before free tier upper bound
    (200000,     FREE_TIER,         None), # at free tier upper bound
    (200001,     ENTRY_TIER,        None), # at entry tier lower bound
    (200002,     ENTRY_TIER,        None), # above entry tier lower bound
    (999999,     ENTRY_TIER,        None), # below entry tier upper bound
    (1000000,    ENTRY_TIER,        None), # at entry tier upper bound
    (1000001,    MID_TIER,          None), # at mid tier lower bound
    (1000002,    MID_TIER,          None), # above mid tier lower bound
    (1999999,    MID_TIER,          None), # below mid tier upper bound
    (2000000,    MID_TIER,          None), # at mid tier upper bound
    (2000001,    UPPER_MIDDLE_TIER, None), # at upper-mid tier lower bound
    (2000002,    UPPER_MIDDLE_TIER, None), # above upper-mid tier lower bound
    (4999999,    UPPER_MIDDLE_TIER, None), # below upper-mid tier upper bound
    (5000000,    UPPER_MIDDLE_TIER, None), # at upper-mid tier upper bound
    (5000001,    HIGH_TIER,         None), # at high tier lower bound
    (5000002,    HIGH_TIER,         None), # above high tier lower bound
    (9999999,    HIGH_TIER,         None), # below high tier upper bound
    (10000000,   HIGH_TIER,         None), # at high tier upper bound
    (10000001,   TOP_TIER,          None), # at top tier lower bound
    (10000002,   TOP_TIER,          None), # above top tier lower bound
    (999999998,  TOP_TIER,          None), # below top tier upper bound ($9,999,999.98)
    (999999999,  TOP_TIER,          None), # at top tier upper bound ($9,999,999.99)
    (1000000000, TOP_TIER,          FeeNotFoundError), # above top tier upper bound ($9,999,999.99)

])
def test_SQLiteFeeManager_get_fee_tier_by_amount(AMOUNT_CENTS:int, EXPECTED_TIER:dict, EXPECTED_EXCEPTION:Exception|None):
    """
    This te
    """
    fee_manager = SQLiteFeeManager()
    if EXPECTED_EXCEPTION is not None:
        with pytest.raises(EXPECTED_EXCEPTION):
            fee_manager.get_transfer_amount_tier(AMOUNT_CENTS)
        return
    fee_tier = fee_manager.get_transfer_amount_tier(AMOUNT_CENTS)
    assert fee_tier.data == EXPECTED_TIER, f"SQLiteFeeManager returned incorrect tier ({fee_tier.data.get('description')}) for amount {AMOUNT_CENTS}, expected '{EXPECTED_TIER.get('description')}'"
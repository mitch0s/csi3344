from api.db.sqlite import connection
from api.object.base import BaseFeeManager, FeeTier


class SQLiteFeeManager(BaseFeeManager):
    def __init__(self):
        super().__init__()

    # declaration required to prevent superclass raising NotImplementedError
    def _load(self):
        pass
    
    @property
    def tiers(self) -> list[FeeTier]:
        conn = connection()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, range_min_cents, range_max_cents, fee_percentage, transfer_cap_cents, description
                FROM "fee"
                ORDER BY range_min_cents ASC
            """)

            rows = cur.fetchall()

            return [
                FeeTier(
                    id=row[0],
                    range_min_cents=row[1],
                    range_max_cents=row[2],
                    fee_percentage=row[3],
                    transfer_cap_cents=row[4],
                    description=row[5],
                )
                for row in rows
            ]

        finally:
            conn.close()
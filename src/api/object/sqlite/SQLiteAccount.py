from api.object.base import BaseAccount
from api.object.sqlite.SQLiteTransfer import SQLiteTransfer
from api.db.sqlite import connection


class SQLiteAccount(BaseAccount):
    def __init__(self, id: int):
        super().__init__(id)

    def _load(self):
        conn = connection()
        try:
            cur = conn.cursor()

            cur.execute(
                """
                SELECT id, user_id, name, created_utc, status
                FROM account
                WHERE id = ?
                """,
                (self.id,)
            )

            row = cur.fetchone()

            if row is None:
                raise Exception("account not found")

            self.id = row[0]
            self.user_id = row[1]
            self.name = row[2]
            self.created_utc = row[3]
            self.status = row[4]

            # compute balance in same query
            cur.execute(
                """
                SELECT COALESCE(SUM(
                        CASE
                            WHEN cr_account_id = ? THEN amount_cents
                            WHEN dr_account_id = ? THEN -amount_cents
                            ELSE 0
                        END
                    ), 0)
                FROM transfer_item
                WHERE cr_account_id = ? OR dr_account_id = ?
                """,
                (self.id, self.id, self.id, self.id)
            )

            balance_row = cur.fetchone()
            self.balance_cents = balance_row[0] if balance_row else 0

        finally:
            conn.close()

    @property
    def transfers(self):
        conn = connection()
        try:
            cur = conn.cursor()

            # only fetch transfer ids, not full data
            cur.execute(
                """
                SELECT DISTINCT t.id
                FROM transfer t
                JOIN transfer_item ti ON ti.transaction_id = t.id
                WHERE ti.cr_account_id = ? OR ti.dr_account_id = ?
                ORDER BY t.created_utc DESC
                """,
                (self.id, self.id)
            )

            rows = cur.fetchall()

            # delegate full loading to SQLiteTransfer
            return [SQLiteTransfer(row[0]) for row in rows]

        finally:
            conn.close()

    @property
    def data(self) -> dict:
        data = self.__dict__.copy()
        data.pop('user_id')
        return data
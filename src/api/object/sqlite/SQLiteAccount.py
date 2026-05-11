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
                "SELECT id, user_id, name, created_utc, status FROM account WHERE id = ?",
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

        finally:
            conn.close()

    @property
    def transactions(self):
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
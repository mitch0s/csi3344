from api.object.base import BaseAccount
from api.db.sqlite import connection

class SQLiteAccount(BaseAccount):
    def __init__(self, id:int):
        super().__init__(id)

    def _load(self):
        """
        load user account from sqlite database
        """
        conn = connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, user_id, name, created_utc, status FROM account WHERE id = ?",
                (self.id,)
            )
            row = cur.fetchone()

            # raise if not found
            if row is None:
                raise Exception("account not found")

            # assign fields
            self.id          = row[0]
            self.user_id     = row[1]
            self.name        = row[2]
            self.created_utc = row[3]
            self.status      = row[4]

        finally:
            conn.close()

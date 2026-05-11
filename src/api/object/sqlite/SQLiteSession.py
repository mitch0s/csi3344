from api.db.sqlite import connection
from api.object.base.BaseSession import BaseSession
from api.object.sqlite.SQLiteUser import SQLiteUser
from api.object.base.errors import SessionNotFound



class SQLiteSession(BaseSession):
    def __init__(self, token:str):
        super().__init__(token)

    def _load(self):
        conn = connection()
        try:
            cur = conn.cursor()

            cur.execute(
                """
                SELECT user_id, created_utc, expiry_utc
                FROM session
                WHERE token = ?
                """,
                (self.token,)
            )

            row = cur.fetchone()

            if row is None : raise SessionNotFound()

            user_id = row[0]
            self.created_utc = row[1]
            self.expiry_utc = row[2]

            # resolve full user object
            self.user = SQLiteUser(user_id)

        finally:
            conn.close()
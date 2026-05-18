import random
from api.db.sqlite import connection
from api.object.base.BaseSession import BaseSession
from api.object.sqlite.sqlite_user import SQLiteUser
from api.object.base.errors import InvalidSessionError
from api.util.dateutil import *

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

            if row is None : raise InvalidSessionError()

            user_id = row[0]
            self.created_utc = row[1]
            self.expiry_utc = row[2]

            # resolve full user object
            self.user = SQLiteUser(user_id)

        finally:
            conn.close()

    @staticmethod
    def create(user: SQLiteUser) -> BaseSession:
        conn = connection()
        try:
            cur = conn.cursor()

            token = 'ses_' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=64))

            created = timestamp_utc()
            expiry = timestamp_utc(h=24)  # 24 hour session

            cur.execute(
                """
                INSERT INTO session (token, user_id, created_utc, expiry_utc)
                VALUES (?, ?, ?, ?)
                """,
                (token, user.id, created, expiry)
            )

            conn.commit()

            # return fully loaded session object
            return SQLiteSession(token)

        finally:
            conn.close()

    def validate_expiry(self) -> None:
        """
        Raise SessionExpiredError if current session exists but is expired.
        """
        if not self.created_utc <= timestamp_utc() <= self.expiry_utc:
            raise InvalidSessionError()

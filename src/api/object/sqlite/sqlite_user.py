import time
from api.util.hashing import *
from api.db.sqlite import connection
from api.object.base.BaseUser import BaseUser
from api.object.base.BaseAccount import BaseAccount
from api.object.sqlite.sqlite_account import SQLiteAccount
from api.object.base.errors import UserNotFoundError, InvalidPasswordError, AccountNotFoundError


class SQLiteUser(BaseUser):
    def __init__(self, id: int):
        super().__init__(id)
        self._accounts = []
        self._last_accounts_check = 0
    def _load(self):
        conn = connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, first_name, last_name, email_address, password_hash, created_utc, status
                FROM user
                WHERE id = ?
                """,
                (self.id,)
            )
            row = cur.fetchone()

            # raise if not found
            if row is None:
                raise UserNotFoundError("user not found")

            self.id = row[0]
            self.first_name = row[1]
            self.last_name = row[2]
            self.email_address = row[3]
            self.password_hash = row[4]
            self.created_utc = row[5]
            self.status = row[6]

        finally:
            conn.close()

    @staticmethod
    def get_by_email_address(email_address: str):
        conn = connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id FROM user WHERE email_address = ?", (email_address,))
            row = cur.fetchone()
            if row is None:
                return None
            return SQLiteUser(row[0])
        finally:
            conn.close()

    def validate_password(self, password:str):
        if not verify_password(password, self.password_hash):
            raise InvalidPasswordError()
        
    def get_account(self, id:int) -> BaseAccount:
        for account in self.accounts:
            if account.id == id:
                return account
        raise AccountNotFoundError(f'User does not own an account with id: {id}')

    @property
    def accounts(self) -> list[BaseAccount]:
        conn = connection()
        if time.time() - self._last_accounts_check > 30:
            self._last_accounts_check = time.time()
            try:
                cur = conn.cursor()
                cur.execute("SELECT id FROM account WHERE user_id = ?", (self.id,))
                rows = cur.fetchall()
                self._accounts = []
                for row in rows:
                    account = SQLiteAccount(row[0])
                    account.owner = self
                    self._accounts.append(account)
            finally:
                conn.close()
        return self._accounts

    @property
    def data(self) -> dict:
        data = self.__dict__.copy()
        data.pop('password_hash')  # remove password hash from data dict
        data.pop('_accounts')
        data.pop('_last_accounts_check')
        return data
from api.db.sqlite import connection
from api.object.base import BaseTransfer, BaseTransferItem, BaseAccount
from api.util.dateutil import timestamp_utc


class SQLiteTransfer(BaseTransfer):
    def __init__(self, id: int):
        self._items = None
        self._amount = None
        super().__init__(id)

    def _load(self):
        conn = connection()
        try:
            cur = conn.cursor()

            cur.execute(
                """
                SELECT id, user_note, created_utc, status
                FROM transfer
                WHERE id = ?
                """,
                (self.id,)
            )

            row = cur.fetchone()

            if row is None:
                raise Exception("transfer not found")
            self.id = row[0]
            self.user_note = row[1]
            self.created_utc = row[2]
            self.status = row[3]
        finally:
            conn.close()

    @property
    def items(self):
        conn = connection()
        try:
            cur = conn.cursor()

            cur.execute(
                """
                SELECT id, transaction_id, cr_account_id, dr_account_id, amount_cents, type
                FROM transfer_item
                WHERE transaction_id = ?
                """,
                (self.id,)
            )

            rows = cur.fetchall()

            items = []
            total = 0

            for row in rows:
                ti = BaseTransferItem()
                ti.id = row[0]
                ti.amount_cents = row[4]
                ti.type = row[5]
                items.append(ti)

                # treat as signed ledger movement if needed
                total += row[4]

            self._items = items
            self._amount = total

            return self._items

        finally:
            conn.close()

    @property
    def amount_cents(self) -> int:
        # ensure items loaded first
        if self._amount is None:
            _ = self.items
        return self._amount
    
    @property
    def data(self) -> dict:
        return {
            'id': self.id,
            'status': self.status,
            'created_utc': self.created_utc,
            'user_note': self.user_note,
            'amount_cents': self.amount_cents,
            'items': [item.data for item in self.items]
        }
    
    @staticmethod
    def create(sender:BaseAccount, receiver:BaseAccount, amount_cents:int, fee_cents:int=0, user_note:str=''):
        """
        creates a transfer.

        each transfer has:
        - 1 user item (actual transfer between accounts)
        - 1 fee item (sender -> system fees account)
        """

        conn = connection()
        try:
            cur = conn.cursor()
            conn.execute("BEGIN")

            # 1. Create transfer header
            cur.execute(
                """
                INSERT INTO transfer (user_note, created_utc, status)
                VALUES (?, ?, ?)
                """,
                (user_note, timestamp_utc(), "pending")
            )

            transfer_id = cur.lastrowid

            # 2. user transfer item (actual money movement)
            cur.execute(
                """
                INSERT INTO transfer_item (transaction_id, cr_account_id, dr_account_id, amount_cents, type)
                VALUES (?, ?, ?, ?, ?)
                """,
                (transfer_id, receiver.id, sender.id, amount_cents, "user")
            )

            # 3. fee transfer item (only if applicable)
            if fee_cents > 0:
                SYSTEM_FEE_ACCOUNT_ID = 0 
                cur.execute(
                    """
                    INSERT INTO transfer_item (transaction_id, cr_account_id, dr_account_id, amount_cents, type)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (transfer_id, SYSTEM_FEE_ACCOUNT_ID, sender.id, fee_cents, "fees")
                )

            conn.commit()
            return SQLiteTransfer(transfer_id)

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    def related_user_ids(self) -> list[int]:
        conn = connection()

        try:
            cur = conn.cursor()

            cur.execute(
                """
                SELECT DISTINCT a.user_id
                FROM transfer_item ti
                JOIN account a ON a.id = ti.cr_account_id
                    OR a.id = ti.dr_account_id
                WHERE ti.transaction_id = ?
                """,
                (self.id,)
            )

            rows = cur.fetchall()

            return [row[0] for row in rows if row[0] is not None]

        finally:
            conn.close()

    def amount_by_account_id(self, id:int):
        pass
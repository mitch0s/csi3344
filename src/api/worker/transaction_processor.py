import asyncio
import traceback

from api.db.sqlite import connection
from api.util.dateutil import timestamp_utc
from api.object.sqlite.sqlite_transfer import SQLiteTransfer
from api.websocket import *

class TransactionProcessor:
    """
    continuously checks pending transfers and marks them as completed
    once incubation period has elapsed.
    """

    CHECK_INTERVAL_SECONDS = 1
    COMPLETE_AFTER_SECONDS = 5

    def __init__(self):
        self.running = False

    async def process_pending_transfers(self) -> list[SQLiteTransfer]:
        """
        Processes pending transfers and returns a list of transfers
        that were marked as processed.
        """

        processed_transfers = []

        conn = connection()

        try:
            cur = conn.cursor()

            # fetch pending transfers
            cur.execute(
                """
                SELECT id, created_utc
                FROM transfer
                WHERE status = 'pending'
                """
            )

            rows = cur.fetchall()

            now = timestamp_utc()

            for row in rows:
                transfer_id = row[0]
                created_utc = row[1]

                expiry_timestamp = timestamp_utc(
                    s=self.COMPLETE_AFTER_SECONDS,
                    timestamp=created_utc
                )

                # iso-8601 utc timestamps compare correctly as strings
                if now >= expiry_timestamp:

                    cur.execute(
                        """
                        UPDATE transfer
                        SET status = 'processed'
                        WHERE id = ?
                        """,
                        (transfer_id,)
                    )

                    transfer = SQLiteTransfer(transfer_id)
                    transfer.status = 'processed'
                    processed_transfers.append(transfer)
                    print(f'transfer {transfer_id} marked complete')

            conn.commit()
            return processed_transfers

        finally:
            conn.close()

    async def run_forever(self):
        """
        async infinite worker loop
        """
        self.running = True
        print('TransactionWorker started')

        while self.running:
            try:
                processed_transfers = await self.process_pending_transfers()
                for transfer in processed_transfers:
                    related_user_ids = transfer.related_user_ids()
                    for websocket in active_websocket_sessions:
                        if not websocket.user.id in related_user_ids:
                            break
                        await websocket.send_transfer_updated_message(transfer)
            except Exception:
                traceback.print_exc()
            await asyncio.sleep(self.CHECK_INTERVAL_SECONDS)

    def stop(self):
        self.running = False




# global instance of transaction processor
g_transaction_processor = TransactionProcessor()
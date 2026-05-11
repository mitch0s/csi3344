import sqlite3

def connection(path: str = 'database.db') -> sqlite3.Connection:
    """
    generate and return a connection object.
    """
    return sqlite3.connect(database=path)


def insert(query: str) -> list:
    conn = connection()
    try:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return [cur.lastrowid]
    finally:
        conn.close()


def select(query: str) -> list:
    conn = connection()
    try:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()
    finally:
        conn.close()
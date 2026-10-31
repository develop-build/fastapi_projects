# Connection and schema setup

import sqlite3

DATABASE_NAME = "transactions.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0 CHECK (balance >= 0)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS transfers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_account_id INTEGER NOT NULL,
                to_account_id INTEGER NOT NULL,
                amount REAL NOT NULL CHECK (amount > 0),
                status TEXT NOT NULL DEFAULT 'completed',
                FOREIGN KEY (from_account_id) REFERENCES accounts(id),
                FOREIGN KEY (to_account_id) REFERENCES accounts(id)
            )
        """)

        conn.commit()

    finally:
        conn.close()
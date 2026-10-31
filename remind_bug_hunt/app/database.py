import sqlite3

DB_PATH = "remind.db"

db = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

db.execute("""
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    due_at TEXT NOT NULL,
    webhook_url TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    retries INTEGER NOT NULL DEFAULT 0
)
""")

db.commit()
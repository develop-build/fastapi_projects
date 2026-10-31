from requests import status_codes
import datetime
import logging
import requests

from fastapi import FastAPI, Request, HTTPException
from app.database import db

app = FastAPI()

log = logging.getLogger("remind")

WEBHOOK_SECRET = "dev-secret-change-me"
MAX_RETRIES = 3

@app.post("/reminders")
async def create_reminder(request: Request):
    data = await request.json()

    db.execute(
        """
        INSERT INTO reminders
        (user_id, message, due_at, webhook_url, status, retries)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data["user_id"],
            data["message"],
            data["due_at"],
            data.get("webhook_url", ""),
            "pending",
            0
        )
    )

    db.commit()

    return {"ok": True}


@app.get("/reminders/{reminder_id}")
async def get_reminder(reminder_id: int):
    row = db.execute(
        "SELECT * FROM reminders WHERE id = ?",
        (reminder_id,)
    ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="id doesn't exist")

    return row


@app.get("/users/{user_id}/reminders")
async def list_reminders(user_id: int):
    return db.execute(
        "SELECT * FROM reminders WHERE user_id = ?",
        (user_id,)
    ).fetchall()


@app.delete("/reminders/{reminder_id}")
async def delete_reminder(reminder_id: int):
    db.execute(
        "DELETE FROM reminders WHERE id = ?",
        (reminder_id,)
    )

    db.commit()

    return {"deleted": reminder_id}


def process_due_reminders():
    now = datetime.datetime.now().isoformat()

    rows = db.execute(
        "SELECT id, message, webhook_url, retries "
        "FROM reminders "
        "WHERE status = 'pending' AND due_at < ?",
        (now,)
    ).fetchall()

    for reminder_id, message, url, retries in rows:
        claim = db.execute(
            """
            UPDATE reminders
            SET status = 'processing'
            WHERE id = ? AND status = 'pending'
            """,
            (reminder_id,)
        )

        db.commit()
        if claim.rowcount == 0:
            continue

        try:
            response = requests.post(
                            url,
                            json={"message": message},
                            headers={
                                "X-Signature": WEBHOOK_SECRET,
                                "Idempotency-Key": str(reminder_id),
                            },
                            timeout=10
                        )
            
            response.raise_for_status()

            db.execute(
                """
                UPDATE reminders
                SET status = 'sent'
                WHERE id = ? AND status = 'processing'
                """,
                (reminder_id,)
            )

        except requests.RequestException as exc:
            log.warning(
                "Failed to send reminder %s: %s",
                reminder_id,
                exc
            )

            if retries < MAX_RETRIES:
                db.execute(
                    """
                    UPDATE reminders
                    SET retries = retries + 1,
                        status = 'pending'
                    WHERE id = ? AND status = 'processing'
                    """,
                    (reminder_id,)
                )
            else:
                db.execute(
                    """
                    UPDATE reminders
                    SET status = 'failed'
                    WHERE id = ? AND status = 'processing'
                    """,
                    (reminder_id,)
                )

        db.commit()

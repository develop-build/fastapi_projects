
from fastapi.testclient import TestClient

from app.main import app
from unittest.mock import Mock, patch
from app.database import db
from app.main import process_due_reminders
import requests

client = TestClient(app)

def test_create_reminder_returns_success():
    response = client.post(
        "/reminders",
        json={
            "user_id": 1,
            "message": "Practice debugging",
            "due_at": "2099-01-01T10:00:00",
            "webhook_url": ""
        }
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_missing_reminder_returns_404():
    response = client.get("/reminders/999999")

    assert response.status_code == 404

def test_process_due_reminders_returns_200():
    cursor = db.execute(
        """
        INSERT INTO reminders
        (user_id, message, due_at, webhook_url, status, retries)
        VALUES(?, ?, ?, ?, ?, ?)
        """,
        (
            1,
            "Test Reminder",
            "2000-01-01T00:00:00",
            "https://example.com/webhook",
            "pending",
            0,
        ),
    )

    reminder_id = cursor.lastrowid
    db.commit()

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None

    with patch("app.main.requests.post", return_value=mock_response):
        process_due_reminders()
    
    row = db.execute(
            "SELECT status, retries FROM reminders WHERE id = ?",
            (reminder_id,),
        ).fetchone()

    assert row == ("sent", 0)

def test_failed_webhook_increments_retries():
    cursor = db.execute(
        """
        INSERT INTO reminders
        (user_id, message, due_at, webhook_url, status, retries)
        VALUES(?, ?, ?, ?, ?, ?)
        """,
        (
            1,
            "Test Reminder",
            "2000-01-01T00:00:00",
            "https://example.com/webhook",
            "pending",
            0,
        ),
    )

    reminder_id = cursor.lastrowid
    db.commit()

    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")

    with patch("app.main.requests.post", return_value=mock_response):
        process_due_reminders()
    
    row = db.execute(
            "SELECT status, retries FROM reminders WHERE id = ?",
            (reminder_id,),
          ).fetchone()

    assert row == ("pending", 1)

def test_reminder_fails_after_max_retries():
    cursor = db.execute(
        """
        INSERT INTO reminders
        (user_id, message, due_at, webhook_url, status, retries)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            1,
            "Retry limit test",
            "2000-01-01T00:00:00",
            "https://example.com/webhook",
            "pending",
            3,
        ),
    )

    reminder_id = cursor.lastrowid
    db.commit()

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError(
        "500 Server Error"
    )

    with patch("app.main.requests.post", return_value=mock_response):
        process_due_reminders()

    row = db.execute(
        "SELECT status, retries FROM reminders WHERE id = ?",
        (reminder_id,),
    ).fetchone()

    assert row == ("failed", 3)

def test_webhook_timeout_increments_retries():
    cursor = db.execute(
        """
        INSERT INTO reminders
        (user_id, message, due_at, webhook_url, status, retries)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            1,
            "Timeout test",
            "2000-01-01T00:00:00",
            "https://example.com/webhook",
            "pending",
            0,
        ),
    )

    reminder_id = cursor.lastrowid
    db.commit()

    with patch(
        "app.main.requests.post",
        side_effect=requests.exceptions.Timeout("Request timed out"),
    ):
        process_due_reminders()

    row = db.execute(
        "SELECT status, retries FROM reminders WHERE id = ?",
        (reminder_id,),
    ).fetchone()

    assert row == ("pending", 1)

def test_already_claimed_reminder_is_skipped():
    cursor = db.execute(
        """
        INSERT INTO reminders
        (user_id, message, due_at, webhook_url, status, retries)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            1,
            "Already claimed reminder",
            "2000-01-01T00:00:00",
            "https://example.com/webhook",
            "processing",
            0,
        ),
    )

    reminder_id = cursor.lastrowid
    db.commit()

    with patch("app.main.requests.post") as mock_post:
        process_due_reminders()

        # The webhook must not be called
        mock_post.assert_not_called()

    row = db.execute(
        "SELECT status, retries FROM reminders WHERE id = ?",
        (reminder_id,),
    ).fetchone()

    assert row == ("processing", 0)

db.execute(
    """
    UPDATE reminders
    SET status = 'processing'
    WHERE id = ? AND status = 'pending'
    """,
    (reminder_id,)
)
db.commit()
from pydantic import Field
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title = "Remind API")

class ReminderCreate(BaseModel):
    title: str = Field(min_length=1)

class ReminderUpdate(BaseModel):
    title: str

reminders = []
next_reminder_id = 1
    
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/reminders")
def create_reminder(reminder : ReminderCreate):
    global next_reminder_id
    new_reminder = {
        "id": next_reminder_id,
        "title": reminder.title,
        "status": "pending",
    }

    reminders.append(new_reminder)
    next_reminder_id += 1
    return new_reminder


@app.get("/reminders")
def get_reminders():
    return reminders

@app.get("/reminders/{reminder_id}")
def get_reminder(reminder_id: int):
    for reminder in reminders:
        if(reminder["id"] == reminder_id):
            return reminder
    raise HTTPException(status_code = 404, detail = "Reminder not found")

@app.put("/reminders/{reminder_id}")
def update_reminder(reminder_id: int, reminder_update: ReminderUpdate):
    for reminder in reminders:
        if(reminder["id"] == reminder_id):
            reminder["title"] = reminder_update.title
            return reminder
    raise HTTPException(status_code = 404, detail = "Reminder not found")

@app.delete("/reminders/{reminder_id}")
def delete_reminder(reminder_id: int):
    for index, reminder in enumerate(reminders):
        if(reminder["id"] == reminder_id):
            reminders.pop(index)
            return {"message": "Reminder deleted"}
    raise HTTPException(status_code = 404, detail = "Reminder not found")

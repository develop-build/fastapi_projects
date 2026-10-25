from pydantic import AllowInfNan
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Task Workflow API")

tasks = {
    1: {
        "id": 1,
        "title": "Learn FastAPI",
        "status": "pending"
    }
}

ALLOWED_TRANSITIONS = {
    "pending": ["in_progress"],
    "in_progress": ["pending", "completed"],
    "completed": []
}

class StatusUpdate(BaseModel):
    status: str

@app.get("/tasks")
def get_all_tasks():
    return tasks

@app.patch("/tasks/{task_id}/status")
def update_task(task_id: int, request: StatusUpdate):
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task Not Found")

    current_status = task["status"]
    new_status = request.status

    if new_status not in ALLOWED_TRANSITIONS:
        raise HTTPException(status_code=400, detail="Invalid status")

    if new_status not in ALLOWED_TRANSITIONS[current_status]:
        raise HTTPException(status_code=400, detail=f"Cannot transition from {current_status} to {new_status}")
    
    task["status"] = new_status
    return task
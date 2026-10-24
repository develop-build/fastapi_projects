from app.models import Task
from app.database import get_db
from app.schemas import TaskCreate, TaskResponse
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Taskflow API is running"}

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title = task_data.title,
        description = task_data.description,
        status = task_data.status
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status

    db.commit()
    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int, db:Session=Depends(get_db)):
    task = db.query(Task).filter(Task.id==task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task Not Found",
        )
    
    db.delete(task)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
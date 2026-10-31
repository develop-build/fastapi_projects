from fastapi import FastAPI, status, HTTPException
from app.schemas import UserCreate

app = FastAPI(title="User CRUD API")

users = []
next_user_id = 1

@app.get("/health")
def test_health():
    return {"status": "ok"}

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    global next_user_id
    new_user = {
        "id": next_user_id,
        "name": user.name,
        "email": user.email,
        "age": user.age
    }

    users.append(new_user)
    next_user_id += 1
    return users

@app.get("/users", status_code=status.HTTP_200_OK)
def get_all_users():
    return users

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not exist"
    )
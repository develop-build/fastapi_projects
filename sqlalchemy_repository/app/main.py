
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, get_db
from app.repositories import UserRepository
from app.schemas import UserCreate, UserResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SQLAlchemy Repository API",
    lifespan=lifespan,
)


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(
    request: UserCreate,
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)

    if repository.get_by_email(request.email):
        raise HTTPException(status_code=409, detail="Email already exists")

    return repository.create(request.name, request.email)


@app.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return UserRepository(db).list_all()


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserRepository(db).get_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    request: UserCreate,
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)

    user = repository.update(
        user_id,
        name=request.name,
        email=request.email,
    )

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not UserRepository(db).delete(user_id):
        raise HTTPException(status_code=404, detail="User not found")

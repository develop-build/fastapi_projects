from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, field_validator

app = FastAPI(title="Pydantic Vaidation")

class User(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=18, le=100)
    email: EmailStr
    bio: str | None = Field(default=None, max_length=200)


    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")

        if value.isdigit():
            raise ValueError("Name cannot contain only digits")

        return value


@app.post("/users")
def create_user(user:User):
    return {
        "status": "success",
        "message": "User created successfully",
        "data": user
    }
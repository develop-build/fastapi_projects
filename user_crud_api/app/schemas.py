from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    age: int = Field(..., ge=18)
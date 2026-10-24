from pydantic import HttpUrl
import re

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class NameRequest(BaseModel):
    name: str

class EmailRequest(BaseModel):
    email: str

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

@app.get("/")
def read_root():
    return {"message": "Welcome to the Validation Engine API!"}

@app.post("/validate/name")
def validate_name(req: NameRequest):
    """Validate if the name is valid (non-empty)"""
    name = req.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    return {"message": "Name is valid", "name": name}


@app.post("/validate/email")
def validate_email(req: EmailRequest):
    """Validate if the email is valid"""
    email = req.email.strip()

    if not email:
        raise HTTPException(status_code=400, detail="Email cannot be empty")

    if not re.fullmatch(EMAIL_PATTERN, email):
        raise HTTPException(status_code=400, detail="Email is not valid")

    return {"message": "Email is valid", "email": email}
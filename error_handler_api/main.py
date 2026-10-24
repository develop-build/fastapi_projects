from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title = "HTTP Error Handler API")

user = {"id": 1, "name": "Deepak"}

class AppException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exception: AppException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": exception.message,
            "status_code": exception.status_code,
            "path": request.url.path
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": exception.detail,
            "status_code": exception.status_code,
            "path": request.url.path
        },
        headers=exception.headers,
    )
    

@app.get("/")
def root():
    return {"message": "app is running"}

@app.get("/users/{user_id}")
def get_users(user_id: int):
    if user_id != user["id"]:
        raise AppException(
            status_code=404,
            message="User not found"
        )
    
    return user

@app.get("/forbidden")
def forbidden():
    raise HTTPException(
        status_code=403,
        detail="You are not allowed to access this resource"
    )
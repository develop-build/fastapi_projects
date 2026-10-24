from pydantic import BaseModel, ConfigDict, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    status: str = "pending"
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str

    model_config = ConfigDict(from_attributes=True)
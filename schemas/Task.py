from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str


class Task(TaskCreate):
    id: int
    completed: bool


class TaskResponse(BaseModel):
    task: Task
    message: str
    success: bool

    model_config = ConfigDict(from_attributes=True)

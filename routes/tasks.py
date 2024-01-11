from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from crud import crud_task
from schemas.Task import TaskCreate, TaskResponse, Task
from config.deps import get_db

router = APIRouter(prefix="/api/tareas", tags=["tasks"])


@router.get("/", response_model=List[Task])
def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_task.get_tasks(db=db, skip=skip, limit=limit)


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud_task.create_task(task=task, db=db)


@router.put("/completar/{task_id}", response_model=TaskResponse)
def mark_task_as_completed(task_id: int, db: Session = Depends(get_db)):
    return crud_task.change_task_status(task_id=task_id, db=db)


@router.delete("/eliminar/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return crud_task.delete_task(task_id=task_id, db=db)


@router.delete("/completadas", status_code=204)
def delete_all_tasks_completed(db: Session = Depends(get_db)):
    return crud_task.delete_all_tasks_completed(db=db)

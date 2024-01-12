from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Type

from models.Task import Task
from schemas.Task import TaskCreate, TaskResponse, Task as TaskSchema


def get_tasks(db: Session, skip: int, limit: int) -> list[Type[Task]]:
    try:
        return db.query(Task).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def create_task(task: TaskCreate, db: Session) -> TaskResponse:
    title = task.title.strip()
    if len(title) < 4:
        raise HTTPException(status_code=400, detail="El título debe tener al menos 4 caracteres")
    
    db_task = db.query(Task).filter(Task.title == title).first()
    if db_task:
        raise HTTPException(status_code=400, detail="La tarea ya existe")

    db_task = Task(title=task.title)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Mapeear Task de modelo de SqlAlchemy a modelo de Pydantic
    task_schema = TaskSchema(id=db_task.id, title=db_task.title, completed=db_task.completed)

    return TaskResponse(task=task_schema, message="Tarea creada correctamente", success=True)


def change_task_status(task_id: int, db: Session) -> TaskResponse:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    task.completed = not task.completed
    db.commit()
    db.refresh(task)

    # mapear Task de modelo de SqlAlchemy a modelo de Pydantic
    task = TaskSchema(id=task.id, title=task.title, completed=task.completed)

    response_message = "Tarea marcada como completada" if task.completed else "Tarea marcada como incompleta"

    return TaskResponse(task=task, message=response_message, success=True)


def delete_task(task_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    db.delete(task)
    db.commit()


def delete_all_tasks_completed(db: Session):
    tasks = db.query(Task).filter_by(completed=True).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No hay tareas completadas")

    for task in tasks:
        db.delete(task)
    db.commit()

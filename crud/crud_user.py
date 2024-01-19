from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from schemas.User import UserCreate, UserUpdate
from models.User import User
from typing import Type

from config.security import get_password_hash


def get_users(db: Session, skip: int, limit: int) -> list[Type[User]]:
    try:
        return db.query(User).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        print(str(e))
        raise HTTPException(status_code=400, detail="Ha ocurrido un error interno. Por favor, inténtalo de nuevo más tarde.")


def get_user_by_id(user_id: int, db: Session) -> Type[User]:
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con id: {user_id} no encontrado")

    return user


def get_user_by_username(username: str, db: Session) -> Type[User]:
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con nombre {username} no encontrado")

    return user


def create_user(user: UserCreate, db: Session) -> Type[User]:
    try:
        with db.begin():
            db_user = db.query(User).filter_by(username=user.username).first()
            if db_user:
                raise HTTPException(status_code=400, detail=f"Nombre de usuario: {user.username} ya existente")

            created_user = User(username=user.username, hashed_password=get_password_hash(user.password))
            db.add(created_user)

        db.refresh(created_user)

        return db.query(User).filter_by(username=created_user.username).first()

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500, detail="Ha ocurrido un error interno. Por favor, inténtalo de nuevo más tarde."
        )


def update_user(user_id: int, user: UserUpdate, db: Session) -> Type[User]:
    db_user = db.query(User).filter_by(id=user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"Usuario con id: {user_id} no encontrado")

    if user.username is not None:
        existing_user = db.query(User).filter_by(username=user.username).first()
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=400, detail=f"Nombre de usuario: {user.username} ya existente")
        db_user.username = user.username
    else:
        raise HTTPException(status_code=400, detail="El campo 'username' no puede ser nulo")

    if user.password is not None:
        db_user.hashed_password = get_password_hash(user.password)
    else:
        raise HTTPException(status_code=400, detail="El campo 'password' no puede ser nulo")

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(user_id: int, db: Session):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con id: {user_id} no encontrado")

    db.delete(user)
    db.commit()

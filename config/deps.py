from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Generator, Type
from sqlalchemy.orm import Session
from jose import jwt

from decouple import config

from crud import crud_user
from models.User import User
from schemas.Token import TokenData
from . import security

from db import SessionLocal


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="token")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> Type[User]:
    """
    Obtiene el usuario actual en función del token de sesión.

    Parámetros:
    - db: La sesión de la base de datos.
    - token: El token de sesión.

    Retorna:
    - User: El usuario con la sesión actual.

    Excepciones:
    - HTTPException: Si el token es inválido o el usuario no existe.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, config("SECRET_KEY"), algorithms=[security.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except jwt.JWTError:
        raise credentials_exception

    user = crud_user.get_user_by_username(username=token_data.username, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Obtiene el usuario actualmente activo.

    Parámetros:
    - current_user: El usuario actual.

    Retorna:
    - User: Usuario con la sesión actual activa.

    Excepciones:
    - HTTPException: Si el usuario no está activo.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")

    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Obtiene el usuario superusuario actualmente activo.

    Parámetros:
    - current_user: El usuario activo actual.

    Retorna:
    - User: Usuario superusuario con la sesión actual activa.

    Excepciones:
    - HTTPException: Si el usuario no está activo o no es superusuario.
    """
    if not current_user.is_super_user:
        raise HTTPException(
            status_code=403, detail="No tienes permisos suficientes"
        )

    return current_user


def init_admin_user():
    db: Session = SessionLocal()

    admin_user = crud_user.get_user_by_username(db=db, username="admin")
    if not admin_user:
        admin_user_data = {
            "username": "admin",
            "password": "admin",
            "is_super_user": True,
        }
        admin_user_create = User(**admin_user_data)
        crud_user.create(db, user=admin_user_create)

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from decouple import config
from sqlalchemy.orm import Session

from crud import crud_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8
ALGORITHM = "HS256"
SECRET_KEY = config("SECRET_KEY")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def authenticate_user(db: Session, username: str, password: str):
    user = crud_user.get_user_by_username(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

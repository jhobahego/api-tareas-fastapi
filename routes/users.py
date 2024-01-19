from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.deps import get_db, get_current_active_superuser, reusable_oauth2
from crud import crud_user
from schemas.User import UserCreate, UserUpdate, User


router = APIRouter(prefix="/api/users", tags=["users"])


# @router.get("/", response_model=list[User])
@router.get("/", response_model=list[User], dependencies=[Depends(get_current_active_superuser)])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)

    return users


@router.get("/{username}", response_model=User)
def get_user_by_username(username: str, db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)):
    user = crud_user.get_user_by_username(username=username, db=db)

    return user


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.create_user(user=user, db=db)

    return db_user


@router.put("/{user_id}", status_code=200, response_model=User)
def update_user(
    user_id: int, user: UserUpdate, db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2)
):
    db_user = crud_user.update_user(user_id=user_id, user=user, db=db)

    return db_user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)):
    crud_user.delete_user(user_id=user_id, db=db)

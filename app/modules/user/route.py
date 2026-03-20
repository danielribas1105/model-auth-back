from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.modules.auth.service import authenticate_user
from app.modules.user.schema import UserCreate, UserResponse, UserUpdate
from app.modules.user.model import User
from app.modules.user import service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def my_profile(user: User = Depends(authenticate_user)):
    """Returns the data of the authenticated user."""
    return user


@router.post("/", response_model=UserResponse, status_code=201)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db, data)


@router.put("/me", response_model=UserResponse)
def update_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
):
    return service.update_user(db, user.id, data)


@router.delete("/me", status_code=204)
def delete_account(
    db: Session = Depends(get_db), user: User = Depends(authenticate_user)
):
    service.delete_user(db, user.id)

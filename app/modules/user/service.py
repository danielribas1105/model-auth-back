from sqlalchemy.orm import Session
from app.modules.user.model import User
from app.modules.user.schema import UserCreate, UserUpdate
from app.core.auth import hash_senha
from fastapi import HTTPException


def create_user(db: Session, data: UserCreate) -> User:
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user = User(
        name=data.name,
        email=data.email,
        senhaHash=hash_senha(data.senha),  # saves the password hash
        image=data.image,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


def update_user(db: Session, user_id: str, data: UserUpdate) -> User:
    user = get_user_by_id(db, user_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: str) -> None:
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()

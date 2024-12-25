from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(User)).scalars().all()
    return users

@router.get("/{user_id}")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    return user

@router.post("/create")
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    user.slug = slugify(user.username)
    db.execute(insert(User).values(**user.dict()))
    db.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

@router.put("/update")
async def update_user(user: UpdateUser, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_to_update = db.execute(select(User).where(User.id == user_id)).scalar()
    if user_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    user_to_update.firstname = user.firstname
    user_to_update.lastname = user.lastname
    user_to_update.age = user.age
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}

@router.delete("/delete")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_to_delete = db.execute(select(User).where(User.id == user_id)).scalar()
    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User was deleted successfully!"}

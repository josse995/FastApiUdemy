import sys
sys.path.append("../TodoApp")

import models
from fastapi import APIRouter, Depends, HTTPException
from .auth import get_db, get_current_user, verify_password, get_password_hash, get_user_exception
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

models.Base.metadata.create_all(bind=engine)

class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str

@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

@router.get('/user/{user_id}')
def get_user_by_id_path(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users)\
        .filter(models.Users.id == user_id)\
        .first()
    if user:
        return user
    return http_exception_not_found()

@router.get('/user/')
def get_user_by_id_query(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users)\
        .filter(models.Users.id == user_id)\
        .first()
    if user:
        return user
    return http_exception_not_found()

@router.put('/user/password')
def user_modify_password(user_verification: UserVerification, user: dict = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user_model = db.query(models.Users)\
        .filter(models.Users.id == user.get('id'))\
        .first()

    if user_model is not None:
        if user_model.username == user_verification.username and verify_password(
                user_verification.password, user_model.hashed_password):
            user_model.hashed_password = get_password_hash(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return successful_response(200)

    raise http_exception_not_found()



@router.delete('/')
def delete_current_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user_model = db.query(models.Users)\
        .filter(models.Users.id == user.get("id"))\
        .first()

    if user_model is None:
        raise http_exception_not_found()

    db.query(models.Users) \
        .filter(models.Users.id == user.get("id")) \
        .delete()

    db.commit()

    return successful_response(200)

def successful_response(status_code: int):
    return {
        'status_code': status_code,
        'transaction': 'Successful'
    }

def http_exception_not_found():
    return HTTPException(status_code=404, detail="User not found")
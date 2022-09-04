import sys
sys.path.append("../TodoApp")

import models
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from .auth import get_db, get_current_user, verify_password, get_password_hash, get_user_exception
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import RedirectResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404:{"detail": "Not found"}}
)

templates = Jinja2Templates(directory="templates")

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

@router.get("/edit-password", response_class=HTMLResponse)
async def edit_user_view(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("edit-user-password.html", {"request": request, "user": user})

@router.post("/edit-password", response_class=HTMLResponse)
async def user_password_change(request: Request, username: str = Form(...), password: str = Form(...),
                               password2: str = Form(...), db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    user_data = db.query(models.Users).filter(models.Users.username == username).first()

    msg = "Invalid username or password"

    if user_data is not None:
        if username == user_data.username and verify_password(password, user_data.hashed_password):
            user_data.hashed_password = get_password_hash(password2)
            db.add(user_data)
            db.commit()
            msg = "Password updated"

    return templates.TemplateResponse("edit-user-password.html", {"request": request, "user": user, "msg": msg})


def successful_response(status_code: int):
    return {
        'status_code': status_code,
        'transaction': 'Successful'
    }

def http_exception_not_found():
    return HTTPException(status_code=404, detail="User not found")
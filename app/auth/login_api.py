from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from app.auth.login_schema import LoginResponse
from app.core.database.database import database
from sqlalchemy.orm import Session
from app.auth.login_service import LoginService as login_service


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(data_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return login_service.login(data_form.username, data_form.password, db)
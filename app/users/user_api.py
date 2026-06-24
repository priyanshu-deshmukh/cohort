from fastapi import APIRouter, Depends
from app.users.user_schema import SignupSchema, UserSignup
from sqlalchemy.orm import Session
from app.core.database.database import database
from app.users.user_service import UserService as user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=SignupSchema)
def signup(signup_request: UserSignup, db: Session = Depends(database.get_db)):
    return user_service.create_new_user(signup_request.email, signup_request.name, signup_request.password, db)
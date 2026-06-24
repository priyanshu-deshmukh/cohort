from fastapi import APIRouter, Depends
from app.users.user_schema import SignupSchema, UserSignup
from sqlalchemy.orm import Session
from app.core.database.database import database
from app.users.user_service import UserService as user_service
from app.models.user import User
from app.utils.role_checker.role_checker import RoleChecker
from enum import Enum

class LoginAs(str, Enum):
    INSTRUCTOR = "INSTRUCTOR"
    STUDENT = "STUDENT"
    COHORT_ADMIN = "COHORT_ADMIN"


router = APIRouter(prefix="/users", tags=["users"])




@router.post("/signup/{role}", response_model=SignupSchema)
def signup(signup_request: UserSignup, role: LoginAs, db: Session = Depends(database.get_db)):
    return user_service.create_new_user(signup_request.email, signup_request.name, signup_request.password, role, db)
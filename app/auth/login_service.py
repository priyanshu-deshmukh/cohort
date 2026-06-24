from sqlalchemy.orm import Session
from app.users.user_repository import UserRepository as user_repository
from fastapi import HTTPException, status
from app.utils.jwt_helper.jwt_helper import JWTHelper
from app.utils.passwords.password_helper import PasswordHelper
from fastapi.responses import JSONResponse


class LoginService:

    @staticmethod
    def login(email: str, password: str, db: Session):
        existing_user = user_repository.get_user_by_email(email, db)

        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = "User not found"
            )
        
        is_verified = PasswordHelper.verify_password(password, existing_user.hashed_password)
        
        if not is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Password."
            )
        
        payload = {
            "user_id": str(existing_user.user_id),
            "name": existing_user.name,
            "email": existing_user.email,
        }

        return {
            "access_token": JWTHelper.encode_token(payload=payload),
            "type": "bearer"
            }
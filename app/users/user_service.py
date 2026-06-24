from sqlalchemy.orm import Session
from app.models.user import User
from app.users.user_repository import UserRepository as user_repository
from fastapi import HTTPException, status
from app.utils.passwords.password_helper import PasswordHelper
import uuid
from app.users.user_schema import GetUserResponse

class UserService:

    @staticmethod
    def create_new_user(email: str, name: str, plain_password: str, db: Session):
        existing_user = user_repository.get_user_by_email(email, db)
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User Already Exists"
            )
        new_user = User(
            email = email,
            name = name,
            hashed_password = PasswordHelper.hash_password(plain_password)
        )
        return user_repository.create_new_user(new_user, db)
    

    @staticmethod
    def get_user_by_user_id(user_id: uuid.UUID, db: Session):
        user = user_repository.get_user_by_user_id(user_id, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found"
            )
        return user
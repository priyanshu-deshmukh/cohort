from sqlalchemy.orm import Session
from app.models.user import User
from app.users.user_repository import UserRepository as user_repository
from fastapi import HTTPException, status
from app.utils.passwords.password_helper import PasswordHelper
import uuid
from app.models.user_role import UserRole
from app.user_roles.user_role_repository import UserRoleRepository as user_role_repository

class UserService:

    @staticmethod
    def create_new_user(email: str, name: str, plain_password: str, role: str, db: Session):
        existing_user = user_repository.get_user_by_email(email, db)
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User Already Exists"
            )
        new_user_record = User(
            email = email,
            name = name,
            hashed_password = PasswordHelper.hash_password(plain_password)
        )

        new_user = user_repository.create_new_user(new_user_record, db)
        if role == "STUDENT":
            new_user_role_record = UserRole(
                user_id = new_user.user_id,
                role_id = "b2900512-c0bd-47e7-b7ff-57916ef5c9a8"
            )
        elif role == "INSTRUCTOR":
            new_user_role_record = UserRole(
                user_id = new_user.user_id,
                role_id = "c14d0343-fbe3-47a8-93f1-2678aad78a7b"
            )
        elif role == "COHORT_ADMIN":
            new_user_role_record = UserRole(
                user_id = new_user.user_id,
                role_id = "558620b4-d03d-4332-a882-2154bbfb344d"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid value for role."
            )
        user_role_repository.create_user_role_record(new_user_role_record, db)
        return new_user
    

    @staticmethod
    def get_user_by_user_id(user_id: uuid.UUID, db: Session):
        user = user_repository.get_user_by_user_id(user_id, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found"
            )
        return user
    
    @staticmethod
    def get_user_email_by_user_id(user_ids: list[uuid.UUID], db: Session):
        return user_repository.get_user_email_by_user_id(user_ids, db)
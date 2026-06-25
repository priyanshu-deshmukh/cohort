from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy import select
import uuid



class UserRepository:

    @staticmethod
    def create_new_user(user: User, db: Session):
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database Error in user_repo.\n\nMore details: {e}"
            )
        
    @staticmethod
    def get_user_by_email(email: str, db: Session):
        return db.execute(select(User).where(User.email == email)).scalars().first()
    
    @staticmethod
    def get_user_by_user_id(user_id: uuid.UUID, db: Session):
        return db.execute(select(User).where(User.user_id == user_id)).scalars().first()
    
    @staticmethod
    def get_user_email_by_user_id(user_ids: list[uuid.UUID], db: Session):
        return db.execute(select(User.email).where(User.user_id.in_(user_ids))).scalars().all()
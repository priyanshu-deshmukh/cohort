from sqlalchemy.orm import Session
import uuid
from sqlalchemy import select
from app.models.user_role import UserRole
from app.models.role import Role
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status



class UserRoleRepository:

    @staticmethod
    def get_roles_for_user(user_id: uuid.UUID, db: Session):
        return db.execute(select(UserRole).where(UserRole.user_id == user_id)).scalars().all()
    
    @staticmethod
    def get_role_names_by_id(role_ids: list[uuid.UUID], db: Session):
        return db.execute(select(Role.role_name).where(Role.role_id.in_(role_ids))).scalars().all()
    

    @staticmethod
    def create_user_role_record(user_role_record: UserRole, db: Session):
        try:
            db.add(user_role_record)
            db.commit()
            db.refresh(user_role_record)
            return user_role_record
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database Error Occured while creating new user role record. more detail: {e}"
            )
        

        
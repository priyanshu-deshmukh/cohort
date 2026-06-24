from sqlalchemy.orm import Session
import uuid
from sqlalchemy import select
from app.models.user_role import UserRole
from app.models.role import Role

class RoleRepository:

    @staticmethod
    def get_roles_for_user(user_id: uuid.UUID, db: Session):
        return db.execute(select(UserRole).where(UserRole.user_id == user_id)).scalars().all()
    
    @staticmethod
    def get_role_names_by_id(role_ids: list[uuid.UUID], db: Session):
        return db.execute(select(Role.role_name).where(Role.role_id.in_(role_ids))).scalars().all()
    

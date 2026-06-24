from fastapi import HTTPException, status
import uuid
from sqlalchemy.orm import Session
from app.user_roles.user_role_repository import RoleRepository as role_repository



class RoleService:

    @staticmethod
    def get_role_names_for_user(user_id: uuid.UUID, db: Session):
        role_ids = [role.role_id for role in role_repository.get_roles_for_user(user_id, db)]
        roles = role_repository.get_role_names_by_id(role_ids, db)
        return roles
    

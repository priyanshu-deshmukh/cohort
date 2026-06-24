from fastapi import HTTPException, status
import uuid
from sqlalchemy.orm import Session
from app.user_roles.user_role_repository import UserRoleRepository as user_role_repository
from app.users.user_service import UserService as user_service
from app.models.user_role import UserRole

class UserRoleService:

    @staticmethod
    def get_role_names_for_user(user_id: uuid.UUID, db: Session):
        role_ids = [role.role_id for role in user_role_repository.get_roles_for_user(user_id, db)]
        roles = user_role_repository.get_role_names_by_id(role_ids, db)
        return roles
    

    @staticmethod
    def assign_role_to_user(user_id: uuid.UUID, role_id: uuid.UUID, db: Session):
        existing_user = user_service.get_user_by_user_id(user_id, db)
        new_user_role_record = UserRole(
            user_id = user_id,
            role_id=role_id
        )
        return user_role_repository.create_user_role_record(new_user_role_record, db)
    
    @staticmethod
    def get_roles_for_user(user_id: uuid.UUID, db: Session):
        return user_role_repository.get_roles_for_user(user_id, db)
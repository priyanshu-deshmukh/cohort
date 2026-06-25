from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.utils.jwt_helper.jwt_helper import JWTHelper
from app.users.user_service import UserService as user_service
from fastapi import HTTPException, status, Depends
from app.core.database.database import database
from app.models.user import User
from app.user_roles.user_role_service import UserRoleService as user_role_service

OAuth2Scheme = OAuth2PasswordBearer("/auth/login")

class RoleChecker:

    @staticmethod
    def get_current_user(token: str = Depends(OAuth2Scheme), db: Session = Depends(database.get_db)):
        payload = JWTHelper.decode_token(token)
        user_id = payload.get("user_id", None)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"sign in first"
            )
        current_user = user_service.get_user_by_user_id(user_id, db)
        return current_user
    

    @staticmethod
    def role_checker(required_roles: list[str]):
        def inner(user: User = Depends(RoleChecker.get_current_user), db: Session = Depends(database.get_db)):
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not authenticated"
                )
            user_roles = user_role_service.get_role_names_for_user(user.user_id, db)
            for role in user_roles:
                if role in required_roles:        
                    return user
                raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Access Denied. You are {user.name} with roles {user_roles}"
                    )
        return inner
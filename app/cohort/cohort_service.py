import uuid
from sqlalchemy.orm import Session
from app.models.cohort import Cohort
from app.cohort.cohort_repository import CohortRepository as cohort_repository
from fastapi import HTTPException, status
from app.models.user import User
from app.user_roles.user_role_service import UserRoleService as user_role_service

class CohortService:

    @staticmethod
    def create_new_cohort(cohort_name: str, cohort_description: str, cohort_admin: uuid.UUID, db: Session):
        
        existing_cohort = cohort_repository.get_cohort_by_admin_id(cohort_admin, db)
        
        if existing_cohort:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can create only One cohort."
            )
        
        new_cohort = Cohort(
            cohort_name = cohort_name,
            cohort_description = cohort_description,
            cohort_admin=cohort_admin
        )
        return cohort_repository.create_new_cohort(new_cohort, db)
    
    @staticmethod
    def delete_cohort(cohort_id: uuid.UUID, user: User, db: Session):
        existing_cohort = cohort_repository.get_cohort_by_cohort_id(cohort_id, db)

        if not existing_cohort:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail="Cohort not found"
            )
        
        if existing_cohort.cohort_admin != user.user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cohort not found"
            )
        
        if existing_cohort.is_deleted == True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cohort is already deleted"
            )
        
        return cohort_repository.delete_cohort(existing_cohort, db)
    

    @staticmethod
    def get_all_active_cohorts(user: User, db: Session):
        user_role = user_role_service.get_role_names_for_user(user.user_id, db)
        if "COHORT_ADMIN" in user_role:
            return cohort_repository.get_cohort_by_admin_id(user.user_id, db)
        cohorts = cohort_repository.get_all_active_cohorts(db)
        return cohorts
    

    @staticmethod
    def get_cohort_by_id(cohort_id: uuid.UUID, db: Session, user: User):
        existing_cohort = cohort_repository.get_cohort_by_cohort_id(cohort_id, db)
        
        if not existing_cohort:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail="Cohort Not Found"
            )
        
        user_roles = user_role_service.get_role_names_for_user(user.user_id, db)
        if "COHORT_ADMIN" in user_roles:
            if existing_cohort.cohort_admin == user.user_id:
                return existing_cohort
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cohort not found"
                )
        return existing_cohort
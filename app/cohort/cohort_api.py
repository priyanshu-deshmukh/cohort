from fastapi import APIRouter, Depends
from app.utils.role_checker.role_checker import RoleChecker
from app.core.database.database import database
from app.models.user import User
from app.cohort.cohort_schema import CohortCreate
from sqlalchemy.orm import Session
from app.cohort.cohort_service import CohortService as cohort_service
import uuid

router = APIRouter(prefix="/cohort", tags=["Cohorts"])


@router.post("/create")
def create_new_cohort(new_cohort: CohortCreate, db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["COHORT_ADMIN"]))):
    return cohort_service.create_new_cohort(new_cohort.cohort_name, new_cohort.cohort_description, user.user_id, db)

@router.delete("/delete/{cohort_id}")
def delete_cohort(cohort_id: uuid.UUID, db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["COHORT_ADMIN"]))):
    return cohort_service.delete_cohort(cohort_id, user, db)

@router.get("/get_all")
def get_all_cohort(db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["SUPERADMIN", "STUDENT", "COHORT_ADMIN"]))):
    return cohort_service.get_all_active_cohorts(user.user_id, db)

@router.get("/{cohort_id}")
def get_cohort_by_id(cohort_id: uuid.UUID, db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["SUPERADMIN", "COHORT_ADMIN", "STUDENT", "INSTRUCTOR"]))):
    return cohort_service.get_cohort_by_id(cohort_id, db, user)
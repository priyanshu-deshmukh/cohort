from fastapi import APIRouter, Depends
from app.core.database.database import database
from app.courses.courses_schema import CourseCreate
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.role_checker.role_checker import RoleChecker
from app.courses.course_service import CourseService as course_service
import uuid 
from app.course_onboarding.course_onboarding_service import CourseOnboardingService as course_onboarding_service

router = APIRouter(prefix="/course", tags=["courses"])


@router.post("/create")
def create_new_course(new_course: CourseCreate, db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["COHORT_ADMIN"]))):
    return course_service.create_new_course(new_course.course_title, new_course.course_description, user.user_id, db)

@router.delete("/delete/{course_id}")
def delete_course(course_id: uuid.UUID, db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["COHORT_ADMIN"]))):
    return course_service.delete_course(course_id, user, db)

@router.get("/all")
def get_all_available_courses(db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["STUDENT"]))):
    return course_service.get_all_available_courses(db)

@router.get("/all_my")
def get_all_my_courses(db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["INSTRUCTOR", "STUDENT", "COHORT_ADMIN"]))):
    return course_service.get_all_courses(db, user)

@router.get("/get_all_students/{course_id}")
def get_all_enrolled_students(course_id: uuid.UUID, db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["COHORT_ADMIN", "INSTRUCTOR"]))):
    return course_onboarding_service.get_students_for_course(course_id, user.user_id, db)


# @router.get("/get_all_students/{cohort_id}")

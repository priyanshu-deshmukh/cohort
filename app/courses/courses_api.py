from fastapi import APIRouter, Depends
from app.core.database.database import database
from app.courses.courses_schema import CourseCreate
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.role_checker.role_checker import RoleChecker
from app.courses.course_service import CourseService as course_service
import uuid 


router = APIRouter(prefix="/course", tags=["courses"])


@router.post("/create")
def create_new_course(new_course: CourseCreate, db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["COHORT_ADMIN"]))):
    return course_service.create_new_course(new_course.course_title, new_course.course_description, user.user_id, db)

@router.delete("/delete/{course_id}")
def delete_course(course_id: uuid.UUID, db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["COHORT_ADMIN"]))):
    return course_service.delete_course(course_id, db)
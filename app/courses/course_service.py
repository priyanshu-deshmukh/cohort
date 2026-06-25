import uuid
from sqlalchemy.orm import Session
from app.models.course import Course
from app.courses.course_repository import CourseRepository as course_repository
from app.models.user import User
from app.cohort.cohort_service import CohortService as cohort_service
from fastapi import HTTPException, status

class CourseService:
    
    @staticmethod
    def create_new_course(course_title: str, course_description: str, created_by: uuid.UUID, db: Session):
        
        cohort = cohort_service.get_all_active_cohorts(created_by, db)
        
        if not cohort:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You don't have any active cohorts. Create one to add courses"
            )

        new_course_object = Course(
            cohort_id = cohort.cohort_id,
            course_title=course_title,
            course_description=course_description,
            created_by=created_by
        )
        return course_repository.create_new_course(new_course_object, db)
    
    @staticmethod
    def delete_course(course_id: uuid.UUID, user: User, db: Session):
        existing_course = course_repository.get_course_by_course_id(course_id, db)

        if existing_course.created_by != user.user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course Not found"
            )
        
        if existing_course.is_deleted == True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course is already deleted."
            )
        
        return course_repository.delete_course(existing_course, db)

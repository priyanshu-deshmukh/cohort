import uuid
from sqlalchemy.orm import Session
from app.models.course import Course
from app.courses.course_repository import CourseRepository as course_repository
from app.models.user import User

class CourseService:
    
    @staticmethod
    def create_new_course(course_title: str, course_description: str, created_by: uuid.UUID, db: Session):
        new_course_object = Course(
            course_title=course_title,
            course_description=course_description,
            created_by=created_by
        )
        return course_repository.create_new_course(new_course_object, db)
    
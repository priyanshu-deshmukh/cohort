from sqlalchemy.orm import Session
from app.models.course import Course
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

class CourseRepository:

    @staticmethod
    def create_new_course(new_course: Course, db: Session):
        try:
            db.add(new_course)
            db.commit()
            db.refresh(new_course)
            return new_course
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database Error occured while creating new course.\n\nMore Detail: {e}"
           )

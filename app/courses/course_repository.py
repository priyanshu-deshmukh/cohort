from sqlalchemy.orm import Session
from app.models.course import Course
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
import uuid
from fastapi.responses import JSONResponse


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

    @staticmethod
    def get_course_by_course_id(course_id: uuid.UUID, db: Session):
        return db.execute(select(Course).where(Course.course_id == course_id)).scalars().first()
    
    @staticmethod
    def delete_course(course: Course, db: Session):
        course.is_deleted == True
        db.commit()
        db.refresh(course)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Course Deleted Successfully"
            }
        )
    
    @staticmethod
    def activate_course(course: Course, db: Session):
        course.is_active = True
        db.commit()
        db.refresh(course)

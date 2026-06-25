from sqlalchemy.orm import Session
from app.models.course import Course
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, and_
import uuid
from fastapi.responses import JSONResponse
from app.models.onboarding import Onboarding

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
        course.is_deleted = True
        course.is_active = False
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

    @staticmethod
    def get_courses_for_my_cohort(user_id: uuid.UUID, db: Session):
        """
        this function fetches all the courses that a cohort admin has created
        """
        courses = db.execute(select(Course).where(Course.created_by == user_id)).scalars().all()
        return courses
    
    @staticmethod
    def get_courses_for_instructor(instructor_id: uuid.UUID, db: Session):
        """
        this function fetches the course to which instructor is assigned to
        """
        courses_ids = db.execute(select(Onboarding.course_id).where(and_(Onboarding.user_id == instructor_id, Onboarding.onboarded_as=="INSTRUCTOR"))).scalars().all()
        courses = db.execute(select(Course).where(Course.course_id.in_(courses_ids))).scalars().all()
        return courses
        #TODO replace scalars().all() to scalars().first() after testing


    @staticmethod
    def get_courses_for_student(student_id: uuid.UUID, db: Session):
        """
        this function fetches all the courses that a student has opted for
        """
        courses_ids = db.execute(select(Onboarding.course_id).where(and_(Onboarding.user_id == student_id, Onboarding.onboarded_as=="STUDENT"))).scalars().all()
        courses = db.execute(select(Course).where(Course.course_id.in_(courses_ids))).scalars().all()
        return courses
    
    @staticmethod
    def get_all_available_courses(db: Session):
        return db.execute(select(Course).where(Course.is_active==True)).scalars().all()
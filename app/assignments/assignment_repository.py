from app.models.assignment import Assignment
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from fastapi import HTTPException, status
import uuid


class AssignmentRepository:

    @staticmethod
    def create_new_assignment(assignment: Assignment, db: Session):
        try:
            db.add(assignment)
            db.commit()
            db.refresh(assignment)
            return assignment
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database Error occured while creating new assignment.\n\nMore details: {e}"
            )
    
    @staticmethod
    def get_assignments_by_course_id(course_id: uuid.UUID, db: Session):
        return db.execute(select(Assignment).where(Assignment.course_id==course_id)).scalars().all()
    
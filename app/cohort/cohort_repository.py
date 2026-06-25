from app.models.cohort import Cohort
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import uuid
from sqlalchemy import select

class CohortRepository:

    @staticmethod
    def create_new_cohort(new_cohort: Cohort, db: Session):
        try:
            db.add(new_cohort)
            db.commit()
            db.refresh(new_cohort)
            return new_cohort
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database Error occured while creating new cohort.\n\nMore details: {e}"
            )
        
    @staticmethod
    def delete_cohort(cohort: Cohort, db: Session):
        cohort.is_deleted = True
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            detail="Cohort Deleted successfully"
        )
    
    @staticmethod
    def get_cohort_by_cohort_id(cohort_id: uuid.UUID, db: Session):
        cohort = db.execute(select(Cohort).where(Cohort.cohort_id == cohort_id)).scalars().first()
        return cohort
    
    @staticmethod
    def get_cohort_by_admin_id(admin_id: uuid.UUID, db: Session):
        return db.execute(select(Cohort).where(Cohort.cohort_admin == admin_id)).scalars().first()
    
    @staticmethod
    def get_all_active_cohorts(db: Session):
        return db.execute(select(Cohort).where(Cohort.is_deleted==False, Cohort.is_active==True)).scalars().all()
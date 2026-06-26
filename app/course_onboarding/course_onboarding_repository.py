from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.onboarding import Onboarding
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import uuid
from app.models.user import User

class CourseOnboardingRepository:

    @staticmethod
    def create_course_onboarding_record(onboarding_record: Onboarding, db: Session):
        try:
            db.add(onboarding_record)
            db.commit()
            db.refresh(onboarding_record)
            return onboarding_record
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database Error occured while creating new onboarding.\n\n more details: {e}"
            )
        
    @staticmethod
    def get_onboarding_record_for_user_course(course_id: uuid.UUID, user_id: uuid.UUID, db: Session):
        onboarding_record = db.execute(select(Onboarding).where(Onboarding.course_id == course_id, Onboarding.user_id==user_id)).scalars().first()
        return onboarding_record
    
    @staticmethod
    def get_all_onboardings_for_course(course_id: uuid.UUID, db: Session):
        onboardings = db.execute(select(Onboarding).where(Onboarding.course_id == course_id)).scalars().all()
        return onboardings
    

    @staticmethod
    def get_all_onboardings_for_user(user_id: uuid.UUID, db: Session):
        onboardings = db.execute(select(Onboarding).where(Onboarding.user_id == user_id)).scalars().all()
        return onboardings
    

    @staticmethod
    def get_students_for_course(course_id: uuid.UUID, db: Session):
        
        onboardings = db.execute(select(Onboarding).where(Onboarding.course_id==course_id, Onboarding.onboarded_as == "STUDENT")).scalars().all()
        
        ids = [onboarding.user_id for onboarding in onboardings]

        raw_users = db.execute(select(User).where(User.user_id.in_(ids))).scalars().all()
        
        users = []
        for user in raw_users:
            i=0
            users.append(
                {
                    "user_id": user.user_id,
                    "email": user.email,
                    "cohort_id": onboardings[i].cohort_id,
                    "course_id": onboardings[i].course_id,
                    "joined_at": onboardings[i].onboarded_at,
                }
            )
            i+=1
        return users
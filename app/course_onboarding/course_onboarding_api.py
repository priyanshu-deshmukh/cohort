from fastapi import APIRouter, Depends
from app.core.database.database import database
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.role_checker.role_checker import RoleChecker
import uuid
from app.course_onboarding.course_onboarding_service import CourseOnboardingService as course_onboarding_service
from app.course_onboarding.course_onboarding_schema import InviteInstructor


router = APIRouter(prefix="/onboard", tags=["Course Onboarding"])

@router.post("/join_course/{course_id}")
def join_course(course_id: uuid.UUID, db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["STUDENT"]))):
    return course_onboarding_service.join_course(course_id, user.user_id, db)

@router.post("/invite_instructor}")
def invite_instructor(invitation: InviteInstructor, db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["COHORT_ADMIN"]))):
    return course_onboarding_service.invite_instructor(invitation.instructor_id, invitation.course_id, user, db)

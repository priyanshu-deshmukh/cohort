from sqlalchemy.orm import Session
import uuid
from app.course_onboarding.course_onboarding_repository import CourseOnboardingRepository as course_onboarding_repository
from fastapi import HTTPException, status
from app.models.onboarding import Onboarding
from app.courses.course_repository import CourseRepository as course_repository
from fastapi.responses import JSONResponse
from app.models.user import User
from app.courses.course_repository import CourseRepository as course_repository



class CourseOnboardingService:

    @staticmethod
    def join_course(course_id: uuid.UUID, user_id: uuid.UUID, db: Session):
        
        existing_onboardings = course_onboarding_repository.get_onboarding_record_for_user_course(course_id, user_id, db)
        
        if existing_onboardings:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already enrolled in the course"
            )

        onboarding_record = Onboarding(
            user_id=user_id,
            course_id=course_id,
            cohort_id=course_repository.get_course_by_course_id(course_id, db).cohort_id,
            onboarded_as="STUDENT",
        )

        new_onboarding = course_onboarding_repository.create_course_onboarding_record(onboarding_record, db)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": f"You have successfully enrolled in the course"
            }
        )
    
    @staticmethod
    def invite_instructor(instructor_id: uuid.UUID, course_id: uuid.UUID, user: User, db: Session):
        
        existing_course = course_repository.get_course_by_course_id(course_id, db)
        
        if not existing_course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        #cohort admin can only add instructors to their course only. not other's
        if existing_course.created_by != user.user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Course Not found"
            )
        existing_onboardings = course_onboarding_repository.get_all_onboardings_for_course(course_id, db)
        for onboarding_record in existing_onboardings:
            if onboarding_record.onboarded_as == "INSTRUCTOR":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Course already has an instructor assigned."
                )
                
        existing_onboardings = course_onboarding_repository.get_onboarding_record_for_user_course(course_id, instructor_id, db)

        #if someone is already enrolled as student, they can not be enrolled as instructor
        if existing_onboardings and existing_onboardings.onboarded_as=="STUDENT":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already enrolled as Student."
            )
        #if someone is already enrolled as the instructor to this course, it is shown
        elif existing_onboardings and existing_onboardings.onboarded_as=="INSTRUCTOR":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already assigned as Instructor."
            )
        
        existing_entries = course_onboarding_repository.get_all_onboardings_for_user(instructor_id, db)

        #if there is already an entry of user in onboardings with INSTRUCTOR role somewhere else, they belong to some other course
        for existing_entry in existing_entries:
            if existing_entry.onboarded_as == "INSTRUCTOR":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User is not available. (teaching somewhere else)"
                )
        

        onboarding_record = Onboarding(
            user_id=instructor_id,
            course_id=course_id,
            cohort_id=course_repository.get_course_by_course_id(course_id, db).cohort_id,
            onboarded_as="INSTRUCTOR",
        )

        onboarding_course_record = course_onboarding_repository.create_course_onboarding_record(onboarding_record, db)
        course_repository.activate_course(existing_course, db)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": f"Instructor successfully Added."
            }
        )
    
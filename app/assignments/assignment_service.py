from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.assignment import Assignment
from app.assignments.assignment_repository import AssignmentRepository as assignment_repository
from fastapi import HTTPException, status, UploadFile
from app.utils.s3_storage_service.s3_service import S3_service
from app.courses.course_repository import CourseRepository as course_repository
from app.course_onboarding.course_onboarding_service import CourseOnboardingService as course_onboarding_service
from app.users.user_service import UserService
from app.utils.ses_email_service.email_service import EmailService


class AssignmentService:

    @staticmethod
    def create_new_assignment(file: UploadFile, assignment_title: str, assignment_description: str, deadline: datetime, total_points: int, user: User, db: Session):
        try:
            assignment_record = Assignment(
            title=assignment_title,
            course_id=(_course := course_repository.get_courses_for_instructor(user.user_id, db)[0]).course_id,
            description=assignment_description,
            deadline=deadline,
            total_points=total_points,
            created_by=user.user_id,
            assignment_ref=S3_service.upload_file(_file_name := f"{assignment_title}_{user.user_id}.{file.filename.split('.')[-1]}", file.filename, "assignment")
        )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something went wrong. more details: {e}"                        
        )
        new_assignment = assignment_repository.create_new_assignment(assignment_record, db)

        course_students_ids = course_onboarding_service.get_onboarded_students_email_for_course(_course.course_id, db)

        user_emails = UserService.get_user_email_by_user_id(course_students_ids, db)

        for email in user_emails:
            EmailService.send_email(email, "New Assignment Created", body=f"New Assignment Created for course {_course.course_title}")
        
        return new_assignment
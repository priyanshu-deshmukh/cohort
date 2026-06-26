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
import uuid
from app.models.submissions import Submission
from fastapi.responses import JSONResponse
from app.models.scores import Score
from langchain.tools import tool

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
            
        
            new_assignment = assignment_repository.create_new_assignment(assignment_record, db)

            course_students_ids = course_onboarding_service.get_onboarded_students_email_for_course(_course.course_id, db)

            user_emails = UserService.get_user_email_by_user_id(course_students_ids, db)
            email_body = f"""
                    New Assignment created for your course {_course.course_title}!

                    Details:

                        Title: {new_assignment.title}
                        Description: {new_assignment.description}
                        Deadline: {new_assignment.deadline}


                    Please ensure prompt submission.
                """
            for email in user_emails:
                EmailService.send_email(email, "New Assignment Created", body=email_body)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something went wrong. more details: {e}"                        
        )
        return new_assignment
    

    @staticmethod
    def submit_assignment(user_id: uuid.UUID, assignment_id: uuid.UUID, remarks: str, file: UploadFile, db: Session):
        if user_id in [assignment.user_id for assignment in assignment_repository.get_all_submissions_for_assignment(assignment_id, db)]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already made a submission"
            )
        try:
            new_submission_record = Submission(
                assignment_id=assignment_id,
                user_id=user_id,
                remarks=remarks,
                submission_ref=S3_service.upload_file(_file_name := f"{file.filename}_{user_id}.{file.filename.split('.')[-1]}", file.filename, "submission")
            )
        
            new_submission = assignment_repository.create_new_submission(new_submission_record, db)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Something went wrong. More details: {e}"
            )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message":"Assignment submitted successfully"
            }
        )
    

    @staticmethod
    def get_all_submissions_for_assignment(assignment_id: uuid.UUID, user_id: uuid.UUID, db: Session):
        assignment = assignment_repository.get_assignment_by_id(assignment_id, db)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="assignment not found"
            )
         
        elif assignment.created_by != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="assignment not found"
            )
        
        else:
            return assignment_repository.get_all_submissions_for_assignment(assignment_id, db)
        
    
    @staticmethod
    def get_all_pending_assignments_for_course(course_id: uuid.UUID, user_id: uuid.UUID, db: Session):
        return assignment_repository.get_all_pending_assignments_for_course(course_id, user_id, db)


    @staticmethod
    def get_all_my_submissions_for_course(course_id: uuid.UUID, user_id: uuid.UUID, db: Session):
        student_ids = [onboarding.user_id for onboarding in course_onboarding_service.get_onboardings_for_course(course_id, db)]
        if user_id not in student_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have not enrolled onto this course."
            )
        return assignment_repository.get_all_my_submissions_for_course(course_id, user_id, db)
    

    @staticmethod
    def grade_assignment(assignment_id: uuid.UUID,  submission_id: uuid.UUID, score: int, remarks: str, user_id: uuid.UUID, db: Session):
        assignment = assignment_repository.get_assignment_by_id(assignment_id, db)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        if assignment.created_by != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        submission = assignment_repository.get_submission_by_id(submission_id, db)
        
        if (submission == None) or (submission.assignment_id != assignment_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Submission not found"
            )
        
        grade_record = Score(
            user_id = submission.user_id,
            assignment_id=assignment_id,
            submission_id = submission_id,
            score=score,
            remarks=remarks
        )

        return assignment_repository.create_grade_record(grade_record, db)
        
    @staticmethod
    # @tool
    def get_all_my_grades_for_course(course_id: uuid.UUID, user_id: uuid.UUID, db: Session) -> list:
        """
        Look up all submissions and returns a list of dict containing assignment_id, submission_id, score,scored_at, remarks.
        """
        return assignment_repository.get_all_my_grades_for_course(course_id, user_id, db)
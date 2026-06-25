from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.assignment import Assignment
from app.assignments.assignment_repository import AssignmentRepository as assignment_repository
from fastapi import HTTPException, status, UploadFile
from app.utils.s3_storage_service.s3_service import S3_service
from app.courses.course_repository import CourseRepository as course_repository


class AssignmentService:

    @staticmethod
    def create_new_assignment(file: UploadFile, assignment_title: str, assignment_description: str, deadline: datetime, total_points: int, user: User, db: Session):
        try:
            assignment_record = Assignment(
            title=assignment_title,
            course_id=course_repository.get_courses_for_instructor(user.user_id, db)[0].course_id,
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
        return assignment_repository.create_new_assignment(assignment_record, db)
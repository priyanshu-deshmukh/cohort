from app.models.assignment import Assignment
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from fastapi import HTTPException, status
import uuid
from app.models.submissions import Submission
from app.models.scores import Score

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
    
    @staticmethod
    def create_new_submission(submission_record: Submission, db: Session):
        try:
            db.add(submission_record)
            db.commit()
            db.refresh(submission_record)
            return submission_record
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database Error occured while craeting new submission. More details: {e}"
            )
    
    @staticmethod
    def get_all_submissions_for_assignment(assignment_id: uuid.UUID, db: Session):
        return db.execute(select(Submission).where(Submission.assignment_id==assignment_id)).scalars().all()

    @staticmethod
    def get_assignment_by_id(assignment_id: uuid.UUID, db: Session):
        return db.execute(select(Assignment).where(Assignment.assignment_id == assignment_id)).scalars().first()
    
    @staticmethod
    def get_all_pending_assignments_for_course(course_id: uuid.UUID, user_id: uuid.UUID, db: Session):
        #gives active assignments
        assignments = db.execute(select(Assignment).where(Assignment.course_id == course_id)).scalars().all()

        #gives submission made
        submissions = db.execute(select(Submission.assignment_id).where(Submission.assignment_id.in_([assignment.assignment_id for assignment in assignments]))).scalars().all()

        final = []

        #gives active assignments - submissions made
        for assignment in assignments:
            if assignment.assignment_id not in submissions:
                final.append({
                    "assignment_id": assignment.assignment_id,
                    "title": assignment.title,
                    "description": assignment.description,
                    "deadline": assignment.deadline,
                    "created_at": assignment.created_at,
                })

        return final
    
    @staticmethod
    def get_all_my_submissions_for_course(course_id: uuid.UUID, user_id: uuid.UUID, db: Session):
        assignments = AssignmentRepository.get_assignments_by_course_id(course_id, db)
        return db.execute(select(Submission).where(Submission.user_id == user_id, Submission.assignment_id.in_([assignment.assignment_id for assignment in assignments]))).scalars().all()
    

    @staticmethod
    def get_submission_by_id(submission_id: uuid.UUID, db: Session):
        return db.execute(select(Submission).where(Submission.submission_id == submission_id)).scalars().first()
    
    @staticmethod
    def create_grade_record(new_grade_record: Score, db: Session):
        try:
            db.add(new_grade_record)
            db.commit()
            db.refresh(new_grade_record)
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database Error occured while creating new Score record. More details: {e}"
            )
        
    @staticmethod
    def get_my_grade(assignment_id: uuid.UUID, db: Session):
        return db.execute(select(Score).where(Score.assignment_id == assignment_id)).scalars().first()
    

    @staticmethod
    def get_all_my_grades_for_course(course_id: uuid.UUID, user_id: uuid.UUID, db: Session):
        submissions = AssignmentRepository.get_all_my_submissions_for_course(course_id, user_id, db)

        scores = db.execute(select(Score).where(Score.submission_id.in_(submission_ids := [submission.submission_id for submission in submissions]))).scalars().all()
        print(submission_ids)
        
        _scores = []

        for submission in submissions:
            i = 0
            if submission.submission_id not in [score.submission_id for score in scores]:
                _scores.append(
                    {
                    "assignment_id": submission.assignment_id,
                    "submission_id": submission.submission_id,
                    "score": "Not Graded Yet",
                    "scored_at": "Not Graded Yet",
                    "remarks": "Not Graded Yet"
                }
                )
                i+=1
            else:
                _scores.append(
                    {
                    "assignment_id": submission.assignment_id,
                    "submission_id": submission.submission_id,
                    "score": scores[i].score,
                    "scored_at": scores[i].scored_at,
                    "remarks": scores[i].remarks
                }
                )
                i += 1

        return _scores
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database.database import database
from app.utils.role_checker.role_checker import RoleChecker
from app.models.user import User
from app.assignments.assignment_service import AssignmentService as assignment_service
from datetime import datetime
import os
from app.core.config.config import settings
import uuid
# from app.utils.agent.agent_service import agent


router = APIRouter(prefix="/assignment", tags=["assignments"])


@router.post("/create_new")
async def create_new_assignment(title: str, description: str, deadline: datetime, points: int, file: UploadFile = File(...), user: User = Depends(RoleChecker.role_checker(["INSTRUCTOR"])), db: Session = Depends(database.get_db)):
   
    with open(file.filename, "wb") as f:
            content = await file.read()
            f.write(content)

    return assignment_service.create_new_assignment(file, title, description, deadline, points, user, db)


@router.post("/submit/{assignment_id}")
async def submit_assignment(assignment_id: uuid.UUID, remarks: str, file: UploadFile = File(...), user: User = Depends(RoleChecker.role_checker(["STUDENT"])), db: Session = Depends(database.get_db)):
    with open(file.filename, "wb") as f:
        content = await file.read()
        f.write(content)
    return assignment_service.submit_assignment(user.user_id, assignment_id, remarks, file, db)

@router.get("/pending/{course_id}")
def get_all_pending_assignments(course_id: uuid.UUID, user: User = Depends(RoleChecker.role_checker(["STUDENT"])), db: Session = Depends(database.get_db)):
     return assignment_service.get_all_pending_assignments_for_course(course_id,user.user_id, db)


@router.get('/get_all_submissions/{assignment_id}')
def get_all_submissions(assignment_id: uuid.UUID, user: User = Depends(RoleChecker.role_checker(["INSTRUCTOR"])), db: Session = Depends(database.get_db)):
    return assignment_service.get_all_submissions_for_assignment(assignment_id, user.user_id, db)

@router.get("/get_all_my_submissions/{course_id}")
def get_all_my_submissions_for_course(course_id: uuid.UUID, db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["STUDENT"]))):
     return assignment_service.get_all_my_submissions_for_course(course_id, user.user_id, db)

@router.post("/grade_assignment/{submission_id}")
def grade_assignment(assignment_id: uuid.UUID, submission_id: uuid.UUID, score: int, remarks: str, user: User = Depends(RoleChecker.role_checker(["INSTRUCTOR"])), db: Session = Depends(database.get_db)):
     return assignment_service.grade_assignment(assignment_id, submission_id, score, remarks, user.user_id, db)


@router.get("/view_all_scores/{course_id}")
def get_all_my_grades_for_course(course_id: uuid.UUID, user: User = Depends(RoleChecker.role_checker(["STUDENT"])), db: Session = Depends(database.get_db)):
    return assignment_service.get_all_my_grades_for_course(course_id, user.user_id, db)

#TODO: Complete this endpoint
# @router.post("/ask_query")
# def ai_agent(query: str):
#     result = agent.invoke({"messages": [{"role": "user", "content": query}]})
#     return result
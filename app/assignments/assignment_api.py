from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database.database import database
from app.utils.role_checker.role_checker import RoleChecker
from app.assignments.assignment_schema import AssignmentCreate
from app.models.user import User
from app.assignments.assignment_service import AssignmentService as assignment_service
from datetime import datetime
import os
from app.core.config.config import settings


router = APIRouter(prefix="/assignment", tags=["assignments"])


@router.post("/create_new")
async def create_new_assignment(title: str, description: str, deadline: datetime, points: int, file: UploadFile = File(...), user: User = Depends(RoleChecker.role_checker(["INSTRUCTOR"])), db: Session = Depends(database.get_db)):
   
    with open(file.filename, "wb") as f:
            content = await file.read()
            f.write(content)

    return assignment_service.create_new_assignment(file, title, description, deadline, points, user, db)
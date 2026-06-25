from fastapi import Depends, APIRouter
from app.core.database.database import database
from app.utils.role_checker.role_checker import RoleChecker
from sqlalchemy.orm import Session
from app.models.user import User
from app.notifications.notification_service import NotificationService as notification_service
import uuid



router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/unread")
def get_unseen_notifications(db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["STUDENT", "INSTRUCTOR", "COHORT_ADMIN"]))):
    return notification_service.get_unseen_notifications(user.user_id, db)

@router.patch("/mark_all_seen")
def mark_all_notification_seen(db: Session = Depends(database.get_db), user: User = Depends(RoleChecker.role_checker(["STUDENT", "INSTRUCTOR", "COHORT_ADMIN"]))):
    return notification_service.mark_notification_seen(user.user_id, db)

@router.post("/create")
def create_new_notification(reciever_id: uuid.UUID, type: str, content: str, db: Session = Depends(database.get_db)):
    return notification_service.create_notification(reciever_id, type, content, db)
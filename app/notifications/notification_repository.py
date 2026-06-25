from sqlalchemy.orm import Session
from app.models.notifications import Notification
import uuid
from sqlalchemy import select, and_
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

class NotificationRepository:
    
    @staticmethod
    def create_notification(notification: Notification, db: Session):
        try:
            db.add(notification)
            db.commit()
            db.refresh(notification)
            return notification
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database Error occured while creating new notification. More details: {e}"
            )


    @staticmethod
    def get_unseen_notifications(user_id: uuid.UUID, db: Session):
        return db.execute(select(Notification).where(and_(Notification.reciever_id == user_id, Notification.seen == False))).scalars().all()
    
    @staticmethod
    def mark_notification_seen(user_id: uuid.UUID, db: Session):
        notifications = NotificationRepository.get_unseen_notifications(user_id, db)

        for notification in notifications:
            notification.seen = True
            db.commit()
            db.refresh(notification)
        if (total:=len(notifications)) == 0:
            return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "No unread messages"}
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"{total} notifications marked as seen"}
        )
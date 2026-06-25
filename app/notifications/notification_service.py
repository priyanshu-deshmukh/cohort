import uuid
from sqlalchemy.orm import Session
from app.notifications.notification_repository import NotificationRepository as notification_repository
from app.models.notifications import Notification


class NotificationService:

    @staticmethod
    def create_notification(reciever_id: uuid.UUID, type: str, content: str, db: Session):
        notification_record = Notification(
            reciever_id=reciever_id,
            type=type,
            content=content,
        )

        return notification_repository.create_notification(notification_record, db)

    @staticmethod
    def get_unseen_notifications(user_id: uuid.UUID, db: Session):
        notifications = notification_repository.get_unseen_notifications(user_id, db)
        return notifications
    
    @staticmethod
    def mark_notification_seen(user_id: uuid.UUID, db: Session):
        return notification_repository.mark_notification_seen(user_id, db)
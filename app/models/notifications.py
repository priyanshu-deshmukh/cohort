from app.core.database.database import Base
from sqlalchemy import Column, Text, func, DateTime, ForeignKey, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
import uuid



class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reciever_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    seen = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

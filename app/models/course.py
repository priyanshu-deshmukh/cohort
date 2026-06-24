from app.core.database.database import Base
from sqlalchemy import Column, String, func, Boolean, DateTime, Text, ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    course_title = Column(String, nullable=False)
    course_description = Column(Text, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
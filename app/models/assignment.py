from app.core.database.database import Base
from sqlalchemy import Column, String, Text, DateTime, func, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid



class Assignment(Base):
    __tablename__ = "assignments"

    assignment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    deadline = Column(DateTime, nullable=False)
    total_points = Column(Integer, nullable=False)
    assignment_ref = Column(String, nullable=False)
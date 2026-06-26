from app.core.database.database import Base
from sqlalchemy import Column, String, DateTime, func, ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID





class Submission(Base):
    __tablename__ = "submissions"

    submission_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignments.assignment_id"), nullable=False)
    submitted_at = Column(DateTime, default=func.now())
    submission_ref = Column(String, nullable=False)
    remarks = Column(String, nullable=True, default="None")
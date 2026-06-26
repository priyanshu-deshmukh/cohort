from app.core.database.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Score(Base):
    __tablename__ = "scores"

    id = Column(UUID(as_uuid = True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignments.assignment_id"), nullable=False)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.submission_id"), nullable=False)
    score = Column(Integer, nullable=True)
    scored_at = Column(DateTime, default=func.now())
    remarks = Column(String, nullable=False, default="None")
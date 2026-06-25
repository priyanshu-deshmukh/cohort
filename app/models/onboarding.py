from app.core.database.database import Base
from sqlalchemy import Column, DateTime, func, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.users.user_api import LoginAs

class Onboarding(Base):
    __tablename__ = "onboardings"
    __table_args__ = (
        UniqueConstraint("user_id", "course_id", name="one_entry_per_course"),
    )
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.course_id"), nullable=False)
    cohort_id = Column(UUID(as_uuid=True), ForeignKey("cohorts.cohort_id", ondelete="CASCADE"), nullable = False)
    onboarded_as = Column(Enum(LoginAs), nullable=False)
    onboarded_at = Column(DateTime, default=func.now())
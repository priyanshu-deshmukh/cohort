from app.core.database.database import Base
from sqlalchemy import Column, String, Text, Boolean, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Cohort(Base):
    __tablename__ = "cohorts"

    cohort_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cohort_name = Column(String, nullable=False)
    cohort_description = Column(Text, nullable=False)
    cohort_admin = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
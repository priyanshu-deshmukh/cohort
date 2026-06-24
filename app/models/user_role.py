from sqlalchemy import Column, ForeignKey, func, DateTime
from app.core.database.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.role_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    assigned_at = Column(DateTime, default=func.now())
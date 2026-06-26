from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class AssignmentCreate(BaseModel):
    assignment_title: str = Field(...)
    assignment_description: str = Field(...)
    deadline: datetime = Field(...)
    total_points: int = Field(...)

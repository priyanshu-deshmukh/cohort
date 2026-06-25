from pydantic import BaseModel, Field
import uuid
from datetime import datetime
class CohortCreate(BaseModel):
    cohort_name: str = Field(..., min_length=4, max_length=30)
    cohort_description: str = Field(..., min_length=5, max_length=50)

class CohortResponse(CohortCreate):
    cohort_admin: uuid.UUID
    created_at: datetime
    
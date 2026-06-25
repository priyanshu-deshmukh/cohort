from pydantic import BaseModel, Field
import uuid

class InviteInstructor(BaseModel):
    course_id: uuid.UUID = Field(..., description="id of course to which instructor is being invited")
    instructor_id: uuid.UUID = Field(..., description="user id of the instructor")
    
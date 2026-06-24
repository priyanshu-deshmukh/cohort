from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    course_title: str = Field(..., min_length=3, max_length=30)
    course_description : str = Field(..., min_length=10, max_length=100)
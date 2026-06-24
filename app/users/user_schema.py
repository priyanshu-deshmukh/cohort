from pydantic import EmailStr, BaseModel, Field
import uuid

class SignupSchema(BaseModel):
    user_id: uuid.UUID
    name: str
    email: EmailStr
    is_active: bool
    is_deleted: bool

class UserSignup(BaseModel):
    email: EmailStr = Field(...)
    name: str = Field(...)
    password: str = Field(..., min_length=8, max_length=30)
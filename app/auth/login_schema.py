from pydantic import BaseModel, EmailStr, Field


class LoginResponse(BaseModel):
    token: str
    type: str = "bearer"
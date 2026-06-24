import jwt
from sqlalchemy.orm import Session
from app.core.config.config import settings

class JWTHelper:

    @staticmethod
    def encode_token(payload: dict):
        return jwt.encode(payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    @staticmethod
    def decode_token(token: str):
        return jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
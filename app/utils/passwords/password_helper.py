from passlib.context import CryptContext

password_context = CryptContext(schemes="bcrypt", deprecated="auto")

class PasswordHelper:

    @staticmethod
    def hash_password(plain_password: str):
        return password_context.hash(plain_password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return password_context.verify(plain_password, hashed_password)
    
    
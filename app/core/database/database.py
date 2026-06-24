from sqlalchemy import create_engine
from app.core.config.config import settings
from fastapi import HTTPException, status
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_engine(url=settings.DB_URL)
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
        pass

class Database:

    @staticmethod
    def get_db():
        db = session()
        try: 
            yield db
        except Exception as e:
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"database error occured.\n\nMore details: {str(e)}"
            )
        finally:
            db.close()


database = Database()
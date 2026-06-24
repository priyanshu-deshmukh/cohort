from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config.config import settings
from fastapi import HTTPException, status
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(url=settings.DB_URL)
session = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
        pass

class Database:

    @staticmethod
    async def get_db():
        async with session() as db:
            try:
                yield db
                await db.commit()
            except Exception as e:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database Error: {str(e)}"
                )
            finally:
                await db.close()


database = Database()
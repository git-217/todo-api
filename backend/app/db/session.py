from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from backend.app.core.config import get_asyncpg_db_url
from sqlalchemy.exc import SQLAlchemyError

DB_URL = get_asyncpg_db_url()
async_engine = create_async_engine(url=DB_URL)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as E:
            await session.rollback()
            raise E
        finally:
            await session.close()
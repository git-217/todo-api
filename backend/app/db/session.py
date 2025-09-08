from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import get_asyncpg_db_url


DB_URL = get_asyncpg_db_url()
async_engine = create_async_engine(url=DB_URL)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_async_session():
    async with async_session() as session:
        yield session
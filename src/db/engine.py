import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.db.models import Base

db_user = os.getenv("POSTGRES_USER", "brenntag_admin")
db_password = os.getenv("POSTGRES_PASSWORD", "root")
db_host = os.getenv("POSTGRES_HOST", "brenntag_db")
db_port = int(os.getenv("POSTGRES_PORT", "5433"))
db_name = os.getenv("POSTGRES_DB", "application_database")

url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(url)


async def create_session() -> AsyncSession:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as sess:
        yield sess

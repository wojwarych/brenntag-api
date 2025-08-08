import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

db_user = os.getenv("POSTGRES_USER", "brenntag_admin")
db_password = os.getenv("POSTGRES_PASSWORD", "root")
db_host = os.getenv("POSTGRES_HOST", "brenntag_db")
db_port = int(os.getenv("POSTGRES_PORT", "5433"))
db_name = os.getenv("POSTGRES_DB", "application_database")

url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(url)


DEFAULT_SESSION_FACTORY = async_sessionmaker(engine, expire_on_commit=False)

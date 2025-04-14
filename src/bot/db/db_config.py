from typing import AsyncGenerator

from environs import Env
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class DBConfig:
    env = Env()
    env.read_env()
    db_url = env.str("DB_URL")

    async_engine = create_async_engine(url=db_url,
                                       # echo=True,
                                       max_overflow=10)
    async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with DBConfig.async_session_factory() as session:
        yield session

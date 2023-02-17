import sqlalchemy
from sqlalchemy import inspect, select

from bot.database.main import Base, engine, async_session, Users


async def register_models():
    async with async_session() as session:
        if await session.execute(select(Users)) is None:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

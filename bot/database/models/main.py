import sqlalchemy
from sqlalchemy import inspect, select

from bot.database.main import Base, engine, async_session, Users


async def register_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

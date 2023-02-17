import sqlalchemy

from bot.database.main import Base, engine


def register_models() -> None:
    if sqlalchemy.inspect(engine).has_table("users") == False:
        Base.metadata.create_all(engine)

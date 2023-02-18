from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:Pesochek06@localhost"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'postgres',
    'password': 'Pesochek06',
    'port': 5432,
    'database': 'postgres'
}

meta = MetaData()

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Users(Base):
    __tablename__ = "users"
    tg_id = Column(BigInteger, primary_key=True)


class Urls(Base):
    __tablename__ = "urls"
    pk = Column(Integer, primary_key=True)
    url = Column(String)


class Scores(Base):
    __tablename__ = 'scores'
    pk = Column(Integer, primary_key=True)
    positive = Column(Integer)
    negative = Column(Integer)
    url = Column(Integer, ForeignKey("urls.pk"))


class Comments(Base):
    __tablename__ = "comments"
    pk = Column(Integer, primary_key=True)
    author = Column(BigInteger, ForeignKey("users.tg_id"))
    url = Column(Integer, ForeignKey("urls.pk"))
    text = Column(String)


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column, Integer, create_engine, String, insert, BigInteger, ForeignKey
import sqlalchemy
from sqlalchemy.orm import Session, relationship

Base = declarative_base()
engine = create_engine('sqlite:///sqlite3.db', echo=True)

meta = MetaData()
MetaData.reflect(meta, bind=engine)

session = Session(bind=engine)


class Users(Base):
    __tablename__ = "users"
    tg_id = Column(BigInteger, primary_key=True)
    comment = Column(String, ForeignKey("comments.pk"))


class Urls(Base):
    __tablename__ = "urls"
    pk = Column(Integer, primary_key=True)
    url = Column(String)
    score = Column(String, ForeignKey("scores.pk"))


class Scores(Base):
    __tablename__ = 'scores'
    pk = Column(Integer, primary_key=True)
    positive = Column(Integer)
    negative = Column(Integer)
    url = Column(String, ForeignKey("urls.pk"))


class Comments(Base):
    __tablename__ = "comments"
    pk = Column(Integer, primary_key=True)
    author = Column(String, ForeignKey("users.tg_id"))
    url = Column(String, ForeignKey("urls.pk"))
    text = Column(String)




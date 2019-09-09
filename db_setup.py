from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Books(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False)
    author = Column(String(250), nullable=False)
    isbn = Column(String(250), nullable=False)
    summary = Column(String)
    comments = Column(String)


engine = create_engine('sqlite:///bookmanager.db')

Base.metadata.create_all(engine)

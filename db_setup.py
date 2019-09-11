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
    comments = Column(Integer)


class Comments(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    comment = Column(String)
    book_id = Column(Integer, ForeignKey('book.id'))
    book = relationship(Books)


# engine = create_engine('sqlite:///bookmanager.db')
engine = create_engine('postgresql://postgres:postgres@localhost:5432/bookmanager')

Base.metadata.create_all(engine)

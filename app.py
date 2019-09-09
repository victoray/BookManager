from flask import Flask, render_template
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Books
from sqlalchemy import create_engine

engine = create_engine('sqlite:///bookmanager.db')
Base.metadata.bind = engine
db_session = sessionmaker(bind=engine)()

app = Flask('__main__')


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
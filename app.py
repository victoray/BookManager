from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from waitress import serve

from db_setup import Base, Books, Comments
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@localhost:5432/bookmanager')
# engine = create_engine('sqlite:///bookmanager.db')
Base.metadata.bind = engine
db_session = sessionmaker(bind=engine)()

app = Flask('__main__')


@app.route('/')
def home():
    books = db_session.query(Books).limit(1000)

    for book in books:
        try:
            book.comments = db_session.query(Comments).filter(Comments.book_id == book.id).count()
            db_session.commit()
        except Exception as e:
            print(e)
            db_session.rollback()

    db_session.close()
    return render_template('index.html', books=books)


@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        for i in range(100):
            book = Books(title=f"{request.form['title']} {i}",
                         author=request.form['author'],
                         isbn=request.form['isbn'],
                         summary=request.form['summary'])

            db_session.add(book)
            db_session.commit()
            db_session.close()

        return redirect(url_for('home'))

    return render_template('add-book.html')


@app.route('/<int:book_id>/delete-book', methods=['POST'])
def delete_book(book_id):
    book = db_session.query(Books).filter(Books.id == book_id).one()
    comments = db_session.query(Comments).filter(Comments.book_id == book_id).all()

    for comment in comments:
        db_session.delete(comment)

    db_session.delete(book)
    db_session.commit()
    db_session.close()
    return redirect(url_for('home'))


@app.route('/<int:book_id>/edit-book', methods=['GET', 'POST'])
def edit_book(book_id):
    book = db_session.query(Books).filter(Books.id == book_id).one()

    if request.method == 'POST':
        book.id = book_id
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form['isbn']
        book.summary = request.form['summary']

        db_session.commit()
        db_session.close()

        return redirect(url_for('home'))

    db_session.close()
    return render_template('edit-book.html', book=book)


@app.route('/<int:book_id>', methods=['POST', 'GET'])
def view_book(book_id):
    book = db_session.query(Books).filter(Books.id == book_id).one()
    comments = db_session.query(Comments).filter(Comments.book_id == book_id).all()

    if request.method == 'POST':
        comment = Comments(comment=request.form['comment'], book_id=book_id)
        db_session.add(comment)
        db_session.commit()
        db_session.close()

        return redirect(url_for('view_book', book_id=book_id))

    db_session.close()
    return render_template('book.html', book=book, comments=comments)


if __name__ == '__main__':
    app.debug = True
    app.run()

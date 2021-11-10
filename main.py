from flask import Flask, render_template, redirect, url_for, request
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
all_books = []

## CREATE DATABASE
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# CREATE TABLE
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        # CREATE RECORD
        new_book = Books(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("add.html")


@app.route("/edit/", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        book_id = request.form["id"]
        book_to_update = Books.query.get(book_id)
        book_to_update.rating = request.form['edit_rating']
        db.session.commit()
        return redirect(url_for('home'))
    else:
        books_id = request.args.get('books_id')
        book_selected = Books.query.get(books_id)

        return render_template("edit.html", book=book_selected)


if __name__ == "__main__":
    app.run(debug=True)

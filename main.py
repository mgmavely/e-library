import flask
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)


all_books = [{'title': i.title, 'author': i.author, 'rating': i.rating} for i in db.session.query(Book).all()]


@app.route('/')
def home():
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if flask.request.method == "POST":
        req = request.form
        new_entry = {
            "title": req.get('title'),
            "author": req.get('author'),
            "rating": req.get('rating')
        }
        all_books.append(new_entry)
        db.session.add(Book(title=req.get('title'), author=req.get('author'), rating=req.get('rating')))
        db.session.commit()
        return render_template('index.html', books=all_books)
    print(db.session.query(Book).all())
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)

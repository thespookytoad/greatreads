import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///goodreads.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        title = request.form.get("title")
        author = request.form.get("author")
        pages = request.form.get("pages")
        genre = request.form.get("genre")
        date = request.form.get("date")
        review = request.form.get("review")
        rating = request.form.get("rating")

        db.execute("INSERT INTO goodreads (name, title, author, pages, genre, date, review, rating) values(?, ?, ?, ?, ?, ?, ?, ?)", name, title, author, pages, genre, date, review, rating)

        return redirect("/")

    else:
        rows = db.execute("SELECT * FROM goodreads")
        return render_template("index.html", rows = rows)


@app.route("/stats", methods=["GET", "POST"])
def stats():
    rows = db.execute("SELECT * FROM goodreads")

    method = request.form.get("method")
    if method == "author":
        rows = db.execute("SELECT * FROM goodreads ORDER BY author ASC;")
    elif method == "rating-one":
        rows = db.execute("SELECT * FROM goodreads ORDER BY rating DESC;")
    elif method == "rating-two":
            rows = db.execute("SELECT * FROM goodreads ORDER BY rating ASC;")
    elif method == "name":
        rows = db.execute("SELECT * FROM goodreads ORDER BY name ASC;")
    elif method == "genre":
        rows = db.execute("SELECT * FROM goodreads ORDER BY genre ASC;")
    elif method == "pages-one":
        rows = db.execute("SELECT * FROM goodreads ORDER BY pages DESC;")
    elif method == "pages-two":
            rows = db.execute("SELECT * FROM goodreads ORDER BY pages ASC;")
    elif method == "date":
        rows = db.execute("SELECT * FROM goodreads ORDER BY date DESC;")
    elif method == "title":
            rows = db.execute("SELECT * FROM goodreads ORDER BY title ASC;")

    return render_template("stats.html", rows = rows)

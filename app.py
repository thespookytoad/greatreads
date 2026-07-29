import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

dbBooks = SQL("sqlite:///goodreads.db")
dbLogin = SQL("sqlite:///login.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
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

        dbBooks.execute("INSERT INTO goodreads (name, title, author, pages, genre, date, review, rating) values(?, ?, ?, ?, ?, ?, ?, ?)", name, title, author, pages, genre, date, review, rating)

        return redirect("/")

    else:
        rows = dbBooks.execute("SELECT * FROM goodreads")
        return render_template("index.html", rows = rows)


@app.route("/stats", methods=["GET", "POST"])
@login_required
def stats():
    rows = dbBooks.execute("SELECT * FROM goodreads")

    method = request.form.get("method")
    if method == "author":
        rows = dbBooks.execute("SELECT * FROM goodreads ORDER BY author ASC;")
    elif method == "rating-one":
        rows = dbBooks.execute("SELECT * FROM goodreads ORDER BY rating DESC;")
    elif method == "rating-two":
        rows = dbBooks.execute("SELECT * FROM goodreads ORDER BY rating ASC;")
    elif method == "name":
        rows = dbBooks.execute("SELECT * FROM goodreads ORDER BY name ASC;")
    elif method == "genre":
        rows = dbBooks.execute("SELECT * FROM goodreads ORDER BY genre ASC;")
    elif method == "pages-one":
        rows = dbBooks.execute("SELECT * FROM goodreads ORDER BY pages DESC;")
    elif method == "pages-two":
        rows = dbBooks.execute("SELECT * FROM goodreads ORDER BY pages ASC;")
    elif method == "date":
        rows = dbBooks.execute("SELECT * FROM goodreads ORDER BY date DESC;")
    elif method == "title":
        rows = dbBooks.execute("SELECT * FROM goodreads ORDER BY title ASC;")

    return render_template("stats.html", rows = rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = dbLogin.execute("SELECT * FROM login WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Please enter username", 400)
        elif not request.form.get("password"):
            return apology("Please enter password", 400)
        elif not request.form.get("confirmation"):
            return apology("Please confirm your password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)

        rows = dbLogin.execute("SELECT * FROM login WHERE username = ?", request.form.get("username"))

        if len(rows) != 0:
            return apology("Username taken", 400)

        dbLogin.execute(
            "INSERT INTO login (username, password, hash) VALUES(?, ?, ?)",
            request.form.get("username"),
            request.form.get("password"),
            generate_password_hash(request.form.get("password"))
        )

        rows = dbLogin.execute("SELECT * FROM login WHERE username = ?", request.form.get("username"))

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")

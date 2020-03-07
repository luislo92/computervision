from flask import Flask, render_template, request, session, redirect, flash, url_for
from .db import *
from tempfile import mkdtemp
from flask_session import Session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def aboutus():
    return render_template("aboutus.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # TODO
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            # TODO
            return render_template("error.html")

        elif not request.form.get("password"):
            # TODO
            return render_template("error.html")

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html")

        session["user_id"] = rows[0]["id"]

        return redirect(url_for("homepage"))

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # TODO
    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("error.html")

        elif not request.form.get("password"):
            return render_template("error.html")

        elif not request.form.get("password") == request.form.get("confirmation"):
            return render_template("error.html")

        hashed_pw = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                 username=request.form.get("username"),
                                 hash=hashed_pw)

        if not new_user_id:
            return render_template("error.html")

        session["user_id"] = new_user_id

        flash("You have been registered")

        return redirect(url_for("homepage"))

    else:
        return render_template("register.html")


@app.route("/homepage", methods=["GET", "POST"])
@login_required
def homepage():
    # TODO
    rows = db.execute("SELECT date_created, food_name, calories FROM (SELECT * FROM transactions WHERE date_created "
                      "BETWEEN date('now', '-7 day') and date('now')) as ts, users, foods WHERE users.user_id = "
                      "ts.user_id AND foods.food_id = ts.food_id")
    return render_template("homepage.html", rows=rows)


@app.route("/scan", methods=["GET", "POST"])
@login_required
def scan():
    # TODO
    pass


@app.route("/logout")
@login_required
def logout():
    # TODO
    session.clear()
    return redirect(url_for("aboutUs"))


@app.route("/profile")
@login_required
def profile():
    # TODO
    return render_template("profile.html")

from flask import Flask, render_template, request, session, redirect
from cs50 import SQL
from tempfile import mkdtemp
from flask_session import Session
from functools import wraps

app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Use CS50 Library to use SQLite3 database
db = SQL("sqlite:///calorievision.db")


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
def aboutUs():
    return render_template("aboutUs.html")


@app.route("/login", methods=["GET", "POST"])
@login_required
def login():
    # TODO
    pass


@app.route("/signUp", methods=["GET", "POST"])
def signUp():
    # TODO
    pass


@app.route("/homepage", methods=["GET", "POST"])
@login_required
def homepage():
    # TODO
    pass


@app.route("/scan", methods=["GET", "POST"])
@login_required
def scan():
    # TODO
    pass

@app.route("/logout")
@login_required
def logout():
    # TODO
    pass

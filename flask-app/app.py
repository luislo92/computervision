from flask import Flask, render_template, request
from cs50 import SQL
from flask_session import Session


app = Flask(__name__)


@app.route("/")
def aboutUs():
    return render_template("aboutUs.html")


@app.route("/login")
def login():
    # TODO
    pass


@app.route("/signUp")
def signUp():
    # TODO
    pass


@app.route("/homepage")
def homepage():
    # TODO
    pass


@app.route("/scan")
def scan():
    # TODO
    pass

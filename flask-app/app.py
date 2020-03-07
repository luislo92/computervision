from flask import Flask, render_template, request
from cs50 import SQL
from flask_session import 

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("homepage.html")

# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
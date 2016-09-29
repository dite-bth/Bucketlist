# all the imports
import os, sys, json
import sqlite3 as lite
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from db_get import get_user

conn = lite.connect('bucketlist.db')

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return 'hejsan'

@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/signin")
def signin():
    return render_template("signin/index.html")

if __name__ == '__main__':
    app.run()
# all the imports
import os, sys, json
import sqlite3 as lite
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from user import User

conn = lite.connect('bucketlist.db')

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return 'hejsan'

@app.route("/profile/<userid>")
def profile(userid):
    user = User(userid)
    return render_template("profile.html", user=user)


@app.route("/main")
def main():
    return render_template("main.html")
@app.route("/signin")
def signin():
    return render_template("signin/index.html")

@app.route('/tricks')

def tricks():
    con = lite.connect('bucketlist.db')
    cursor = con.execute('SELECT trick_name FROM trickslist')
    return render_template('tricks.html', items=cursor.fetchall())

if __name__ == '__main__':
    app.run(debug=True)


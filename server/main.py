import os, sys, json
import sqlite3 as lite
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
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
    con = lite.connect('bucketlist.db')
    con.text_factory = str
    cursor = con.execute('SELECT * FROM trickslist')
    result = cursor.fetchall()
    tricks = list()
    print result
    for item in result:
        trick = Trick(item[0], item[1], item[2], item[3])
        tricks.append(trick)
    return render_template("profile.html", user=user, tricks=tricks)



@app.route("/main")
def main():
    return render_template("main.html")
@app.route("/signin")
def signin():
    return render_template("signin/index.html")

if __name__ == '__main__':
    app.run(debug=True)


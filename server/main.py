# -*- coding: utf-8 -*-
# all the imports
import os, sys, json
import sqlite3 as lite
from user import User
from trick import Trick
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_oauth import OAuth
from urllib2 import Request, urlopen, URLError
import key






# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

SECRET_KEY = 'development key'
DEBUG = True



app.secret_key = SECRET_KEY
oauth = OAuth()

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=key.GOOGLE_CLIENT_ID,
                          consumer_secret=key.GOOGLE_CLIENT_SECRET)

conn = lite.connect('bucketlist.db')




@app.route('/')
def index():
    return render_template("main.html")


@app.route("/googlelogin")
def googlelogin():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    access_token = access_token[0]

    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()
        #'(INSERT res.read INTO user VALUES (value1,value2,value3))'
    # TODO: använd res.read()
    return render_template("main.html")

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
    return render_template("signin.html")

@app.route('/login')
def login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route(key.REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')

if __name__ == '__main__':
    app.run(debug=True)


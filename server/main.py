# -*- coding: utf-8 -*-
# all the imports
import os, sys, json
import sqlite3 as lite
from user import User
from trick import Trick
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, json
from flask_oauth import OAuth
from urllib2 import Request, urlopen, URLError
from wtforms import Form, StringField, SubmitField
import key

from wtforms import Form, TextAreaField, validators, StringField, SubmitField




# create our little application 🙂
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


class RegisterForm(Form):
    name = StringField('nick', validators=[validators.required()])
    email = StringField('email', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = StringField('password', validators=[validators.required(), validators.Length(min=3, max=35)])


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
    jsondata = json.loads(res.read())
    email = jsondata['email']
    print email

    #printar ut email i jsonsträng.

    #Ny kod:

    email = request.form['email']
    print(email)
    conn = lite.connect('bucketlist.db')
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM user WHERE email=?", (email,))
    if not result:

       #databaskoppling
        conn = lite.connect('bucketlist.db')
        c = conn.cursor()
        c.execute("INSERT INTO user (email,nick,password) VALUES (?,?,?)",(email,'NULL','NULL'))
        conn.commit()
        conn.close()

    return render_template("googlelogin.html")



@app.route("/profile/<userid>")
def profile(userid):
    user = User(userid)
    con = lite.connect('bucketlist.db')
    con.text_factory = str
    cursor = con.execute('SELECT * FROM trickslist WHERE trick_type = "flip"')
    result = cursor.fetchall()
    flip_tricks = list()
    for item in result:
        trick = Trick(item[0], item[1], item[2], item[3])
        flip_tricks.append(trick)
    cursor = con.execute('SELECT * FROM trickslist WHERE trick_type = "grind"')
    result = cursor.fetchall()
    grind_tricks = list()
    for item in result:
        trick = Trick(item[0], item[1], item[2], item[3])
        grind_tricks.append(trick)
    cursor = con.execute('SELECT * FROM trickslist WHERE trick_type = "grab"')
    result = cursor.fetchall()
    grab_tricks = list()
    for item in result:
        trick = Trick(item[0], item[1], item[2], item[3])
        grab_tricks.append(trick)
    return render_template("profile.html", user=user, flip_tricks=flip_tricks, grind_tricks=grind_tricks, grab_tricks=grab_tricks)

@app.route("/main")
def main():
    return render_template("main.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method== 'GET':
        return render_template("signin.html")
    elif request.method == 'POST':
        conn = lite.connect('bucketlist.db')
        conn.text_factory = str
        cur = conn.cursor()
        if request.form['email'] == "" or request.form['password'] == "":
            return redirect(url_for('signin'))
        email = request.form['email']
        password = request.form['password']
        cur.execute("SELECT * FROM user WHERE email=?", (email,))
        result = cur.fetchone()
        if not result:
            conn.close()
            error = 'Invalid Credentials. Please try again.'
            return redirect(url_for('main'))
        if password == result[3]:
            conn.close()
            return redirect("profile/%s" % (result[0],))
        else:
            conn.close()
            error = 'Invalid Credentials. Please try again.'
            return redirect(url_for('main'))


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


@app.route("/register", methods=['GET', 'POST'])
def hello():
    form = RegisterForm(request.form)
    print form.errors

    if request.method == 'POST':
        pname = request.form['nick']
        ppassword = request.form['password']
        pemail = request.form['email']
        conn = lite.connect('bucketlist.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO user (nick, email, password) VALUES (?,?,?)", (pname, pemail, ppassword))
        conn.commit()
        conn.close()
        print pname, " ", pemail, " ", ppassword, " ",

        if form.validate():
            # Save the comment here.
            flash('Thanks for registration ' + pname)

        else:
            flash('Error: All the form fields are required. ')

    return render_template("register.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)


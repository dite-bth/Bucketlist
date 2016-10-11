import os

import config
from flask import Flask, render_template, request, session

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return "Hello!"

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form["username"])
        POST_PASSWORD = str(request.form["password"])

        query = "SELECT email, password, firstname FROM admin WHERE email='%s'" % POST_USERNAME

        print(query)

        config.cur.execute(query)

        result = config.cur.fetchall()
        for i in result:

            if i[0] == POST_USERNAME and i[1] == POST_PASSWORD:
                session['logged_in'] = True
                return home()
            elif POST_USERNAME != i[0]:
                return "Wrong Username"
            elif POST_PASSWORD != i[1]:
                return "Wrong Password"

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return do_admin_login()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)

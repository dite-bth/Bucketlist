from flask import Flask, render_template, flash, request
from wtforms import Form, TextAreaField, validators, StringField, SubmitField
import sqlite3 as lite
import wtforms_sqlalchemy
import sys

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class RegisterForm(Form):
    name = StringField('nick', validators=[validators.required()])
    email = StringField('email', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = StringField('password', validators=[validators.required(), validators.Length(min=3, max=35)])


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = RegisterForm(request.form)
    print form.errors

    if request.method == 'POST':
        pname = request.form['name']
        ppassword = request.form['password']
        pemail = request.form['email']
        con = lite.connect("bucketlist.db")
        cur = con.cursor()
        cur.execute("INSERT INTO user (nick, email, password) VALUES (?,?,?)", (pname, pemail, ppassword))
        con.commit()
        con.close()
        print pname, " ", pemail, " ", ppassword, " ",

        if form.validate():
            # Save the comment here.
            flash('Thanks for registration ' + pname)

        else:
            flash('Error: All the form fields are required. ')

    return render_template('register.html', form=form)


'''@app.route('/')
def register_in_database(name, email, password):
        cur.connection('bucketlist.db')
        cur.execute('INSERT INTO users (name, email, password)VALUES("","","")')
        try:
            print name, email, password

        finally:
            con.commit()
            con.close()'''

if __name__ == "__main__":
    app.run()



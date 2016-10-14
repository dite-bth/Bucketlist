from flask import Flask, render_template, flash, request
from wtforms import Form, validators, StringField
import sqlite3 as lite


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class RegisterForm(Form):
    name = StringField('nick', validators=[validators.required()])
    email = StringField('email', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = StringField('password', validators=[validators.required(), validators.Length(min=3, max=35)])


@app.route("/register", methods=['GET', 'POST'])
def hello():
    form = RegisterForm(request.form)
    print form.errors

    if request.method == 'POST':
        pname = request.form['nick']
        ppassword = request.form['password']
        pemail = request.form['email']
        con = lite.connect("bucketlist.db")
        cur = con.cursor()
        cur.execute('INSERT INTO user (nick, email, password) VALUES (?,?,?)', (pname, pemail, ppassword))
        con.commit()
        con.close()
        print pname, " ", pemail, " ", ppassword, " ",

        if form.validate():
            # Save the comment here.
            flash('Thanks for registration ' + pname)

        else:
            flash('Error: All the form fields are required. ')

    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run()



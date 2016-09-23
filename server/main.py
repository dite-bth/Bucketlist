# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
    return 'hejsan'

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """initalizes the database"""
    init_db()
    print 'Initilized the database'

def get_db():
    """Opens a new database connetion if there is none yet for the current application context."""

    if not hasattr(g, 'sqlite_db'):
        g.splite_db = connect_db()
        return g.splite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the databaase again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



if __name__ == '__main__':
    app.run()
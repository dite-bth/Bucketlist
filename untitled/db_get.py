import sqlite3 as lite
import sys

conn = lite.connect('bucketlist.db')

with conn:
    username = conn.cursor()
    username.execute("SELECT nick FROM user WHERE user_id=1")

    username = username.fetchall()
    json.loads(username)

    for row in username:
        print username

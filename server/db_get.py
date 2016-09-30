import sqlite3 as lite
import sys

conn = lite.connect('bucketlist.db')

class get_user():
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")

    result = cursor.fetchall()
    print result[1]
    for user in result:
        print user[1]


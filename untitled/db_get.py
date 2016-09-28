import sqlite3 as lite
import sys

conn = lite.connect('bucketlist.db')

with conn:
    cur = conn.cursor()

    cur.execute("SELECT * FROM user")

    rows = cur.fetchall()

    for row in rows:
        print row

def getUser(uid):
    #Gör DB-uppslag
    return user

def saveUser(user)
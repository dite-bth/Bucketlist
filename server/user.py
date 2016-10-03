import sqlite3 as lite
import sys


class User:
    def __init__(self, userid):
        self.nick = ""
        self.email = ""
        self.dbcon = lite.connect('bucketlist.db')
        self.user_id = userid

        cursor = self.dbcon.cursor()
        cursor.execute("SELECT nick, email FROM user WHERE user_id=?", (userid,))
        result = cursor.fetchone()
        if result == None:
            print "Couldn't find any user in database"

        self.nick = result[0]
        self.email = result[1]

    def getNick(self):
        return self.nick

    def getEmail(self):
        return self.email

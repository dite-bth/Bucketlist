import sqlite3 as lite
import sys

conn = lite.connect('bucketlist.db')

class User:
    def __int__(self, dbcon, userid):
        self.nick = ""
        self.email = ""
        self.dbcon = dbcon
        self.user_id = userid

        with self.dbcon:
            cursor = dbcon.cursor()
            cursor.execute("SELECT * FROM user")
            result = cursor.fetchall()
            self.user_id = result
            return result[1]


    def getNick(self):
        return self.nick

    def getEmail(self):
        return self.email


user = User()
print user.nick
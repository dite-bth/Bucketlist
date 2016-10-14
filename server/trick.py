import sqlite3 as lite
import sys


class Trick:
    def __init__(self, trickid, name=None, url=None, trick_type=None):
        self.trick_name = ""
        self.trick_url = ""
        self.trick_type = ""
        self.trick_id = trickid

        if name == None:
            self.dbcon = lite.connect('bucketlist.db')
            cursor = self.dbcon.cursor()
            cursor.execute("SELECT * FROM trickslist WHERE trick_id=?",(trickid))
            result = cursor.fetchone()
            self.trick_name = result[1]
        else:
            self.trick_name = name
            self.trick_url = url
            self.trick_type = trick_type

    def getName(self):
        return self.trick_name

    def getUrl(self):
        return self.trick_url
<<<<<<< HEAD
=======

    def getType(self):
        return self.trick_type
>>>>>>> master

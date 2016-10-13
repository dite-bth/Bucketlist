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


        if trick_type == 'flip':
            self.dbcon = lite.connect('bucketlist.db')
            cursor = self.dbcon.cursor()
            cursor.execute("SELECT trick_name FROM trickslist WHERE trick_type='flip'")
            result2 = cursor.fetchall()
            self.trick_name = result2[0]





    def getName(self, trick_type):
        return self.trick_name

    def getUrl(self):
        return self.trick_url

    def getType(self):
        return self.trick_type
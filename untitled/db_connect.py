



#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
conn = sqlite3.connect('bucketlist.db')
user_data = [('apa', 'apa@gmail.com'),
                    ('apa', 'apan@gmail.com'),
                    ('john', 'apa@gmail.com'),
                    ('James', 'apa@gmail.com'),
                    ('Eric', 'apa@gmail.com')]

con = sqlite3.connect(":memory:")
c = conn.cursor()

c.execute('''CREATE TABLE user
             (user_id INTEGER PRIMARY KEY,
              nick varchar(20) NOT NULL,
              email varchar(20) NOT NULL)''')
c.executemany('INSERT INTO user(nick, email) VALUES (?,?)', user_data)

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

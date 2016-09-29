import sqlite3
conn = sqlite3.connect('bucketlist.db')
user_data = [('apa', 'apa@gmail.com', 'howdyhoey'),
                    ('apa', 'apan@gmail.com', 'lol'),
                    ('john', 'apa@gmail.com', 'lol2'),
                    ('James', 'apa@gmail.com', 'lol3'),
                    ('Eric', 'apa@gmail.com', 'lol4')]

con = sqlite3.connect(":memory:")
c = conn.cursor()

c.execute('''CREATE TABLE if not exists user
             (user_id INTEGER PRIMARY KEY,
              nick varchar(20) NOT NULL,
              email varchar(48) NOT NULL,
              password varchar(20) NOT NULL)''')
c.executemany('INSERT INTO user(nick, email, password) VALUES (?, ?, ?)', user_data)

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
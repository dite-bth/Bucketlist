import sqlite3
conn = sqlite3.connect('bucketlist.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE user
             (nick, email)''')

# Insert a row of data
c.execute("INSERT INTO user VALUES ('apa','apa@gmail.com')")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
# -- create an sqlite3 db table and populate it -- #


import sqlite3

# Create a new db if the db doesn't already exist
with sqlite3.connect('blog.db') as connection:

    # Get a cursor object to execute sql commands
    c = connection.cursor()

    # Create the table
    c.execute("CREATE TABLE posts (title TEXT, post TEXT)")

    # Insert dummy data into table
    c.execute("INSERT INTO posts VALUES('First Post', 'First post dummy text')")
    c.execute("INSERT INTO posts VALUES('Second Post', 'Second post dummy text')")
    c.execute("INSERT INTO posts VALUES('Third Post', 'Third post dummy text')")
    c.execute("INSERT INTO posts VALUES('Fourth Post', 'Fourth post dummy text')")

# -- Blog controller -- #

import os
from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps

# Configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard_to_guess'

app = Flask(__name__)

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

# Function for connecting to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# A login required decorator
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
        
    return wrap

# View for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = "Invalid credentials. Please try again."
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error)

# View for logged out page (redirects to login view once complete)
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

# View for adding posts
@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not title or not post:
        flash('All fields are required. Please try again')
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute("INSERT INTO posts (title, post) VALUES(?, ?)", [title, post])
        g.db.commit()
        g.db.close()
        flash('New entry was successfully added')
        return redirect(url_for('main'))

# View for main page of blog
@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute("SELECT * FROM posts")
    posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html', posts=posts)

# Runs app if called directly (i.e. not if imported by another module)
if __name__ == '__main__':
    app.run(debug=True)
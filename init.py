# Equivalent to NodeJS Require
import sqlite3
from flask import Flask, render_template, request, g, url_for, redirect #g is for db
from flask.ext.script import Manager
from contextlib import closing

# DB Config
DATABASE = '/tmp/test.db'
DEBUG = True
SECRET_KEY = 'devkey'
USERNAME = 'admin'
PASSWORD = 'default'

# Startup and namespace
app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

manager = Manager(app)

# DB Startup
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

# Handle Requests via Router Hooks?
@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

# Routes
@app.route("/")
def landing():
	cur = g.db.execute('select title, text from entries order by id desc') # SQL commands >_<. Hopefully the ORM is good for complex queries
	entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]

	return render_template("landing/landing.jade",entries=entries)

@app.route('/add', methods=['POST']) # Or we can POST old-school with AJAX
def create_entry():
	g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
	g.db.commit()
	return redirect(url_for('landing'))

# With Manager you can add command line commands
# This command (runserver) runs the server
@manager.command
def runserver():
	app.run()

from commands.compile import manager as compilers
manager.add_command('compile', compilers)

if __name__ == '__main__':
	manager.run()



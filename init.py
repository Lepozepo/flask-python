# Equivalent to NodeJS Require
import sqlite3
from flask import Flask, render_template, request, g, url_for, redirect #g is for db
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

# Compilers
if app.debug:
	import os
	import codecs
	import coffeescript

	# pip install git+https://github.com/imiric/flask-sass.git#egg=flask-sass
	from scss import Scss

	for root, sub_directories, files in os.walk("templates/"):
		for file in files:
			# COFFEESCRIPT
			if file.endswith(".coffee"):
				source_path = root + "/" + file
				destination_directory = "static/js/" + root.replace("templates/","")
				destination_path = destination_directory + "/" + file.replace(".coffee",".js")

				# Create directories if they don't exist
				if not os.path.exists(destination_directory):
					os.makedirs(destination_directory)

				source_data = codecs.open(source_path,"r",encoding="utf-8").read()
				compiled_data = coffeescript.compile(source_data)

				destination_data = codecs.open(destination_path,"w",encoding="utf-8")
				destination_data.write(compiled_data)
				destination_data.close()

			# SCSS
			if file.endswith(".scss"):
				scss = Scss()

				source_path = root + "/" + file
				destination_directory = "static/css/" + root.replace("templates/","")
				destination_path = destination_directory + "/" + file.replace(".scss",".css")

				# Create directories if they don't exist
				if not os.path.exists(destination_directory):
					os.makedirs(destination_directory)

				source_data = codecs.open(source_path,"r",encoding="utf-8").read()
				compiled_data = scss.compile(source_data)

				destination_data = codecs.open(destination_path,"w",encoding="utf-8")
				destination_data.write(compiled_data)
				destination_data.close()



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

	return render_template("landing/landing.html",entries=entries)

@app.route('/add', methods=['POST']) # Or we can POST old-school with AJAX
def create_entry():
	g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
	g.db.commit()
	return redirect(url_for('landing'))

# @app.route("/hello/")
# @app.route("/hello/<name>")
# def hello(name=None):
# 	return render_template("hello.html",name=name)

if __name__ == '__main__':
	app.run()



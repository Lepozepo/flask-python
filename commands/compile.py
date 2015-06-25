from flask.ext.script import Manager
manager = Manager(usage="Compiles CoffeeScript and SCSS")

import os
import codecs
import coffeescript

# pip install git+https://github.com/imiric/flask-sass.git#egg=flask-sass
from scss import Scss

def _scss(file,root):
	SCSS = Scss()

	source_path = root + "/" + file
	destination_directory = "static/css/" + root.replace("templates/","")
	destination_path = destination_directory + "/" + file.replace(".scss",".css")

	# Create directories if they don't exist
	if not os.path.exists(destination_directory):
		os.makedirs(destination_directory)

	source_data = codecs.open(source_path,"r",encoding="utf-8").read()
	compiled_data = SCSS.compile(source_data)

	destination_data = codecs.open(destination_path,"w",encoding="utf-8")
	destination_data.write(compiled_data)
	destination_data.close()

def _coffee(file,root):
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


@manager.command
def all():
	for root, sub_directories, files in os.walk("templates/"):
		for file in files:

			# If file in _ directory then ignore
			parent_directories = root.split("/")
			for directory in parent_directories:
				if directory.startswith("_"):
					continue

			# If file has _ then ignore
			if file.startswith("_"):
				continue

			# COFFEESCRIPT
			if file.endswith(".coffee"):
				_coffee(file,root)

			# SCSS
			if file.endswith(".scss"):
				_scss(file,root)

@manager.command
def scss():
	for root, sub_directories, files in os.walk("templates/"):
		for file in files:

			# If file in _ directory then ignore
			parent_directories = root.split("/")
			for directory in parent_directories:
				if directory.startswith("_"):
					continue

			# If file has _ then ignore
			if file.startswith("_"):
				continue

			# SCSS
			if file.endswith(".scss"):
				_scss(file,root)

@manager.command
def coffee():
	for root, sub_directories, files in os.walk("templates/"):
		for file in files:

			# If file in _ directory then ignore
			parent_directories = root.split("/")
			for directory in parent_directories:
				if directory.startswith("_"):
					continue

			# If file has _ then ignore
			if file.startswith("_"):
				continue

			# COFFEESCRIPT
			if file.endswith(".coffee"):
				_coffee(file,root)





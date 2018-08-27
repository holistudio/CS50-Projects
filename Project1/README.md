# Project 1

Web Programming with Python and JavaScript

## templates folder

Contents:
* layout.html - General layout inherited by all other pages. Include header and navigation bar for login/registration/logout.
* index.html - Homepage for the site. Search bar will only appear after users log in.
* login.html - Login page. Error messages will flash if username or password is invalid. A link to register a new user is also provided.
* register.html - Registration page. Error messages will flash if username already exists or passwords entered do not match. 
* results.html - Search results page. Links displayed for each book with parts of title, author, or ISBN matching search query.
* book.html - Book information page with Goodreads rating and user reviews.

## application.py
The main Flask/SQLAlchemy application. In addition to routing to the above files, an API route is also written for returning book information as JSON given an ISBN (e.g. .../api/<ISBN>)

## books.csv
CSV file containing information on all books in the website's PostgreSQL database.

## import.py
Python code for importing the above CSV file into the PostgreSQL database.

## requirements.txt
Text file containing required pip packages that need to be installed for running the Flask application.
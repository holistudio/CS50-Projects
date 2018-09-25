import os
import requests

from flask import Flask, session, render_template, request, url_for, flash, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
	search = request.form.get("search")
	#ignore case for the search query
	searchResults = db.execute("SELECT * FROM books WHERE LOWER(title) LIKE LOWER(:search) OR LOWER(author) LIKE LOWER(:search) OR isbn LIKE :search", {"search": f"%{search}%"}).fetchall();
	return render_template("results.html", searchResults= searchResults)

@app.route("/book/<isbn>", methods=["GET","POST"])
def book(isbn):
	#find book
	book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone();

	#if it's a post request, add the review to the review table
	if request.method == "POST":
		rating = int(request.form.get("rating"))
		text = request.form.get("text")
		#test if user is signed in
		if 'username' not in session:
			flash("Please sign in first")
		else:
			user_id = db.execute("SELECT * FROM users WHERE username = :username", {"username": session['username']}).fetchone().id;
			#test if user has already submitted a review for this book
			if db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id", {"user_id": user_id, "book_id": book.id}).rowcount == 0:
				db.execute ("INSERT INTO reviews (book_id, user_id, rating, text) VALUES ((SELECT id from books WHERE id=:book_id), (SELECT id from users WHERE id=:user_id), :rating, :text)", {"book_id": book.id, "user_id": user_id, "rating": rating, "text": text})
				db.commit()
			else:
				flash("Users may only comment on a book once")			
		
	#find book's associated reviews
	reviews = db.execute("SELECT * FROM reviews JOIN users ON reviews.user_id=users.id WHERE book_id = :book_id", {"book_id": book.id}).fetchall();
				
	#goodreads API for obtaining average rating and number of reviews
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv("GOODREADS_KEY"), "isbns": {book.isbn}})
	if res.status_code != 200:
		avg_rating = "N/A"
		numReviews = "N/A"
		raise Exception("ERROR: API request unsuccessful.")
	else:
		data= res.json()
		avg_rating = data["books"][0]["average_rating"]
		numReviews = data["books"][0]["work_ratings_count"]
	
	return render_template("book.html", book=book, reviews=reviews, avg_rating=avg_rating, numReviews=numReviews)
@app.route("/api/<isbn>", methods=["GET"])
def api(isbn):
	#find book in database with exact isbn and return a JSON

	query = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn})

	if query.rowcount == 0:
		return jsonify({"error": "ISBN not found"}), 404 #error response code
	book = query.fetchone()
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv("GOODREADS_KEY"), "isbns": {book.isbn}})
	if res.status_code != 200:
		avg_rating = "N/A"
		numReviews = "N/A"
		raise Exception("ERROR: API request unsuccessful.")
	else:
		data= res.json()
		avg_rating = float(data["books"][0]["average_rating"])
		numReviews = data["books"][0]["work_ratings_count"]
	
	return jsonify(title=book.title,author=book.author,year=book.year,isbn=book.isbn,review_count=numReviews,average_score=avg_rating)

@app.route("/login", methods=["GET","POST"])
def login():
	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("pw")
		
		#Invalid username or password cases
		usernameCheck = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount != 0
		passwordCheck = False;

		if usernameCheck:
			passwordCheck = db.execute("SELECT password FROM users WHERE username = :username", {"username": username}).fetchone()[0] == password
		if usernameCheck and passwordCheck:
			session['username'] = request.form['username']
			return redirect(url_for('index'))
		else:
			return render_template("login.html", message="Invalid username or password")
	return render_template("login.html", message="")

@app.route("/logout")
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))


@app.route("/register", methods=["GET","POST"])
def register():
	if request.method =="POST":

	    # Get form information.
	    username = request.form.get("username")
	    password = request.form.get("pw")
	    confirm = request.form.get("pw-conf")

	    #make sure password match
	    if password != confirm:
	    	return render_template("register.html", message="Passwords do not match")
		
	    #make sure username does not already exist
	    if (db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0):
	    	#add username and password to database
	    	db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
	    	flash("You're registered! Please log in.")
	    	db.commit()
	    	return redirect(url_for('index')) 
	    else:
	    	#render within the registration template this message
	    	return render_template("register.html", message="Username already exists")
	    	
	else:
		return render_template("register.html", message="")

if __name__ == "__main__":
    app.run(debug=True)
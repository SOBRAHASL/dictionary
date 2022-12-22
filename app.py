"""
A dictionary based on free databases and APIs
The purpose of this project is the creation of a comprehensive dictionary from different sources
For now, it only uses one source --> https://dictionaryapi.dev/
"""

# Import libraries
from flask import Flask, redirect, render_template, request, jsonify, session
from helpers import lookup, load, suggest, accent
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import os

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///dictionary.db")

# Custom filter
app.jinja_env.filters["accent"] = accent

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search") # Search for the word's meaning
def search():
    
    word = request.args.get("word")
    if not word:
        return render_template("message.html", message="Provide word")
    
    meaning = lookup(word)
    if not meaning:
        return render_template("message.html", message="The word is not found")

    # Record the word
    try:
        if session["user_id"]:
            db.execute("INSERT INTO history (user_id, word) VALUES (?, ?)", session["user_id"], word.lower())
    except:
        None

    return render_template("search.html", meaning=meaning, word=word)


# Load word list
words = load("wordlist/english.txt")
@app.route("/suggestion") # Suggest incomplete word
def suggestion():
    word = request.args.get("word")
    if word:
        suggestion = suggest(words, word.lower(), 2, 4)
    else:
        suggestion = []
        
    return jsonify(suggestion)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Define username, password, confirmation
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return render_template("message.html", message="Provide username")

        # Ensure password was submitted
        elif not password:
            return render_template("message.html", message="Provide password")

        # Ensure confirmation was submitted
        elif not confirmation:
            return render_template("message.html", message="Provide password confirmation")

        # Ensure password matches confirmation
        elif password != confirmation:
            return render_template("message.html", message="Passwords do not match")

        # Ensure username has not been taken
        elif len(db.execute("SELECT * FROM users WHERE username = ?", username)):
            return render_template("message.html", message="Username has already been taken")

        # Insert into table new user
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, generate_password_hash(password))

        # Set user_id as cookie ( session )
        session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", username)[0]["user_id"]

        return render_template("message.html", message="Successful")

    # User reached route via GET
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("message.html", message="Provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("message.html", message="Provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return render_template("message.html", message="Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Message Signed in
        return render_template("message.html", message="Signed in")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Message logged out 
    return render_template("message.html", message="Logged out")

@app.route("/history")
def history():
    try:
        history = db.execute("SELECT DISTINCT word, user_id FROM history WHERE user_id = ?", session["user_id"])
    except:
        history = None

    return render_template("history.html", history=history)

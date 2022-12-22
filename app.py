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
    
    # Example data for offline purposes
    """
    word = "big"
    meaning = [{'word': 'big', 'phonetic': '/bɪɡ/', 'phonetics': [{'text': '/bɪɡ/', 'audio': 'https://api.dictionaryapi.dev/media/pronunciations/en/big-uk.mp3', 'sourceUrl': 'https://commons.wikimedia.org/w/index.php?curid=9014281', 'license': {'name': 'BY 3.0 US', 'url': 'https://creativecommons.org/licenses/by/3.0/us'}}, {'text': '/bɪɡ/', 'audio': 'https://api.dictionaryapi.dev/media/pronunciations/en/big-us.ogg', 'sourceUrl': 'https://commons.wikimedia.org/w/index.php?curid=112420547', 'license': {'name': 'BY-SA 3.0', 'url': 'https://creativecommons.org/licenses/by-sa/3.0'}}], 'origin': 'Something for the beta', 'meanings': [{'partOfSpeech': 'noun', 'definitions': [{'definition': 'Someone or something that is large in stature', 'synonyms': [], 'antonyms': []}, {'definition': 'An important or powerful person; a celebrity; a big name.', 'synonyms': [], 'antonyms': []}, {'definition': '(as plural) The big leagues, big time.', 'synonyms': [], 'antonyms': []}, {'definition': '(BDSM) The participant in ageplay who acts out the older role.', 'synonyms': [], 'antonyms': []}], 'synonyms': ['major leagues'], 'antonyms': ['little']}, {'partOfSpeech': 'verb', 'definitions': [{'definition': 'To praise, recommend, or promote.', 'synonyms': [], 'antonyms': []}], 'synonyms': [], 'antonyms': []}, {'partOfSpeech': 'adjective', 'definitions': [{'definition': 'Of great size, large.', 'synonyms': ['ample', 'huge', 'jumbo', 'large', 'massive', 'sizeable', 'stoor'], 'antonyms': ['little', 'miniature', 'minuscule', 'minute', 'small', 'tiny'], 'example': 'Elephants are big animals, and they eat a lot.'}, {'definition': '(of an industry or other field, often capitalized) Thought to have undue influence.', 'synonyms': [], 'antonyms': [], 'example': 'Big Tech'}, {'definition': 'Popular.', 'synonyms': ['all the rage', 'in demand', 'well liked'], 'antonyms': [], 'example': 'That style is very big right now in Europe, especially among teenagers.'}, {'definition': 'Adult.', 'synonyms': ['adult', 'fully grown', 'grown up'], 'antonyms': ['little', 'young'], 'example': 'Kids should get help from big people if they want to use the kitchen.'}, {'definition': 'Fat.', 'synonyms': ['chubby', 'plus-size', 'rotund'], 'antonyms': [], 'example': 'Gosh, she is big!'}, {'definition': 'Important or significant.', 'synonyms': ['essential', 'paramount', 'weighty'], 'antonyms': [], 'example': "What's so big about that? I do it all the time."}, {'definition': '(with on) Enthusiastic (about).', 'synonyms': ['fanatical', 'mad', 'worked up'], 'antonyms': [], 'example': "I'm not big on the idea, but if you want to go ahead with it, I won't stop you."}, {'definition': 'Mature, conscientious, principled; generous.', 'synonyms': [], 'antonyms': [], 'example': "I tried to be the bigger person and just let it go, but I couldn't help myself."}, {'definition': 'Well-endowed, possessing large breasts in the case of a woman or a large penis in the case of a man.', 'synonyms': ['busty', 'macromastic', 'stacked'], 'antonyms': [], 'example': 'Whoa, Nadia has gotten pretty big since she hit puberty.'}, {'definition': '(sometimes figurative) Large with young; pregnant; swelling; ready to give birth or produce.', 'synonyms': ['full', 'great', 'heavy'], 'antonyms': [], 'example': 'She was big with child.'}, {'definition': 'Used as an intensifier, especially of negative-valence nouns', 'synonyms': [], 'antonyms': [], 'example': 'You are a big liar.\u2003 Why are you in such a big hurry?'}, {'definition': '(of a city) populous', 'synonyms': [], 'antonyms': []}, {'definition': "(of somebody's age) old, mature. Used to imply that somebody is too old for something, or acting immaturely.", 'synonyms': [], 'antonyms': []}], 'synonyms': ['adult', 'fully grown', 'grown up', 'all the rage', 'in demand', 'well liked', 'ample', 'huge', 'jumbo', 'large', 'massive', 'sizeable', 'stoor', 'busty', 'macromastic', 'stacked', 'chubby', 'plus-size', 'rotund', 'essential', 'paramount', 'weighty', 'fanatical', 'mad', 'worked up', 'full', 'great', 'heavy'], 'antonyms': ['little', 'miniature', 'minuscule', 'minute', 'small', 'tiny', 'little', 'young']}, {'partOfSpeech': 'adverb', 'definitions': [{'definition': 'In a loud manner.', 'synonyms': [], 'antonyms': []}, {'definition': 'In a boasting manner.', 'synonyms': [], 'antonyms': [], 'example': "He's always talking big, but he never delivers."}, {'definition': 'In a large amount or to a large extent.', 'synonyms': [], 'antonyms': [], 'example': 'He won big betting on the croquet championship.'}, {'definition': 'On a large scale, expansively.', 'synonyms': [], 'antonyms': [], 'example': "You've got to think big to succeed at Amalgamated Plumbing."}, {'definition': 'Hard.', 'synonyms': [], 'antonyms': [], 'example': 'He hit him big and the guy just crumpled.'}], 'synonyms': [], 'antonyms': []}], 'license': {'name': 'CC BY-SA 3.0', 'url': 'https://creativecommons.org/licenses/by-sa/3.0'}, 'sourceUrls': ['https://en.wiktionary.org/wiki/big']}, {'word': 'big', 'phonetic': '/bɪɡ/', 'phonetics': [{'text': '/bɪɡ/', 'audio': 'https://api.dictionaryapi.dev/media/pronunciations/en/big-uk.mp3', 'sourceUrl': 'https://commons.wikimedia.org/w/index.php?curid=9014281', 'license': {'name': 'BY 3.0 US', 'url': 'https://creativecommons.org/licenses/by/3.0/us'}}, {'text': '/bɪɡ/', 'audio': 'https://api.dictionaryapi.dev/media/pronunciations/en/big-us.ogg', 'sourceUrl': 'https://commons.wikimedia.org/w/index.php?curid=112420547', 'license': {'name': 'BY-SA 3.0', 'url': 'https://creativecommons.org/licenses/by-sa/3.0'}}], 'meanings': [{'partOfSpeech': 'verb', 'definitions': [{'definition': 'To inhabit; occupy', 'synonyms': [], 'antonyms': []}, {'definition': 'To locate oneself', 'synonyms': [], 'antonyms': []}, {'definition': 'To build; erect; fashion', 'synonyms': [], 'antonyms': []}, {'definition': 'To dwell; have a dwelling', 'synonyms': [], 'antonyms': []}], 'synonyms': [], 'antonyms': []}], 'license': {'name': 'CC BY-SA 3.0', 'url': 'https://creativecommons.org/licenses/by-sa/3.0'}, 'sourceUrls': ['https://en.wiktionary.org/wiki/big']}, {'word': 'big', 'phonetic': '/bɪɡ/', 'phonetics': [{'text': '/bɪɡ/', 'audio': 'https://api.dictionaryapi.dev/media/pronunciations/en/big-uk.mp3', 'sourceUrl': 'https://commons.wikimedia.org/w/index.php?curid=9014281', 'license': {'name': 'BY 3.0 US', 'url': 'https://creativecommons.org/licenses/by/3.0/us'}}, {'text': '/bɪɡ/', 'audio': 'https://api.dictionaryapi.dev/media/pronunciations/en/big-us.ogg', 'sourceUrl': 'https://commons.wikimedia.org/w/index.php?curid=112420547', 'license': {'name': 'BY-SA 3.0', 'url': 'https://creativecommons.org/licenses/by-sa/3.0'}}], 'meanings': [{'partOfSpeech': 'noun', 'definitions': [{'definition': 'One or more kinds of barley, especially six-rowed barley.', 'synonyms': [], 'antonyms': []}], 'synonyms': [], 'antonyms': []}], 'license': {'name': 'CC BY-SA 3.0', 'url': 'https://creativecommons.org/licenses/by-sa/3.0'}, 'sourceUrls': ['https://en.wiktionary.org/wiki/big']}, {"word":"hello","phonetics":[{"audio":"https://api.dictionaryapi.dev/media/pronunciations/en/hello-au.mp3","sourceUrl":"https://commons.wikimedia.org/w/index.php?curid=75797336","license":{"name":"BY-SA 4.0","url":"https://creativecommons.org/licenses/by-sa/4.0"}},{"text":"/həˈləʊ/","audio":"https://api.dictionaryapi.dev/media/pronunciations/en/hello-uk.mp3","sourceUrl":"https://commons.wikimedia.org/w/index.php?curid=9021983","license":{"name":"BY 3.0 US","url":"https://creativecommons.org/licenses/by/3.0/us"}},{"text":"/həˈloʊ/","audio":""}],"meanings":[{"partOfSpeech":"noun","definitions":[{"definition":"\"Hello!\" or an equivalent greeting.","synonyms":[],"antonyms":[]}],"synonyms":["greeting"],"antonyms":[]},{"partOfSpeech":"verb","definitions":[{"definition":"To greet with \"hello\".","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]},{"partOfSpeech":"interjection","definitions":[{"definition":"A greeting (salutation) said when meeting someone or acknowledging someone’s arrival or presence.","synonyms":[],"antonyms":[],"example":"Hello, everyone."},{"definition":"A greeting used when answering the telephone.","synonyms":[],"antonyms":[],"example":"Hello? How may I help you?"},{"definition":"A call for response if it is not clear if anyone is present or listening, or if a telephone conversation may have been disconnected.","synonyms":[],"antonyms":[],"example":"Hello? Is anyone there?"},{"definition":"Used sarcastically to imply that the person addressed or referred to has done something the speaker or writer considers to be foolish.","synonyms":[],"antonyms":[],"example":"You just tried to start your car with your cell phone. Hello?"},{"definition":"An expression of puzzlement or discovery.","synonyms":[],"antonyms":[],"example":"Hello! What’s going on here?"}],"synonyms":[],"antonyms":["bye","goodbye"]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/hello"]}]
    """

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

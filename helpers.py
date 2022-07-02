# Import required libraries
import requests
import re

def lookup(word):
    """Look up meaning for symbol."""

    # Contact API
    try: 
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        return response.json()
    except (KeyError, TypeError, ValueError):
        return None


def load(address):
    words = list() # Empty list
    
    # Open the file as read mode
    try:
        file = open(address, "r")
        
        # Add word to words
        for line in file:
            words.append(line.rstrip())
        file.close()
        return words
    except:
        return None


def suggest(words, word, start, n):
    try:
        if len(word) >= start:
            rc = re.compile(f"{word}.*")
            suggestions = list(filter(rc.match, words))
            return suggestions[:n]
    except:
        return None


def accent(text):
    try:
        if re.search("-uk", text):
            return "britain"
        elif re.search("-us", text):
            return "american"
        elif text:
            return "global"
        else:
            return ""
    except:
        return None

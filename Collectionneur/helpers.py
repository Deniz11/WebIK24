import csv
import urllib.request
from cs50 import SQL

from flask import redirect, render_template, request, session
from functools import wraps

from imdbpie import Imdb
imdb = Imdb()

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")

def test(username):

    return db.execute("SELECT * FROM users WHERE username = :username", username=username)

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def valid_id(imdb_id):
    """checks if valid imdb_id"""

    # check if imdb_id stars starts with valid 2 startings characters
    if not (imdb_id[:2] not in ['tt']):

        # return true if id exist else false
        try:
            imdb.validate_imdb_id(imdb_id)
            return True

        except:
            return False

    # if id does not start with valid character return false
    else:
        return False

def valid_id_actor(imdb_id):
    """checks if valid imdb_id of actor, these functions are split because search movie sometimes returns an actor. You can filter that checking if the id does not start with nm"""

    # check if imdb_id stars starts with valid 2 startings characters
    if not (imdb_id[:2] not in ['nm']):

        # return true if id exist else false
        try:
            imdb.validate_imdb_id(imdb_id)
            return True

        except:
            return False

    # if id does not start with valid character return false
    else:
        return False


def only_signs(s):
    """checks if string contains only special characters"""

    for character in s:

        if character.isalnum():
            return True

    return False

def split_community_search(s):
    "return list with found community and community to search"

    split_location = s.find("__````@#$!^$@#86afsdc")

    # remove __````@#$!^$@#86afsdc and put 2 words in tuple
    return (s[:split_location], s[split_location:].replace("__````@#$!^$@#86afsdc", ""))
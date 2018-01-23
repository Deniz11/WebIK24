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


def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


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


def lookup(symbol):
    """Look up quote for symbol."""

    # reject symbol if it starts with caret
    if symbol.startswith("^"):
        return None

    # reject symbol if it contains comma
    if "," in symbol:
        return None

    # query Yahoo for quote
    # http://stackoverflow.com/a/21351911
    try:

        # GET CSV
        url = f"http://download.finance.yahoo.com/d/quotes.csv?f=snl1&s={symbol}"
        webpage = urllib.request.urlopen(url)

        # read CSV
        datareader = csv.reader(webpage.read().decode("utf-8").splitlines())

        # parse first row
        row = next(datareader)

        # ensure stock exists
        try:
            price = float(row[2])
        except:
            return None

        # return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
        return {
            "name": row[1],
            "price": price,
            "symbol": row[0].upper()
        }

    except:
        pass

    # query Alpha Vantage for quote instead
    # https://www.alphavantage.co/documentation/
    try:

        # GET CSV
        url = f"https://www.alphavantage.co/query?apikey=NAJXWIA8D6VN6A3K&datatype=csv&function=TIME_SERIES_INTRADAY&interval=1min&symbol={symbol}"
        webpage = urllib.request.urlopen(url)

        # parse CSV
        datareader = csv.reader(webpage.read().decode("utf-8").splitlines())

        # ignore first row
        next(datareader)

        # parse second row
        row = next(datareader)

        # ensure stock exists
        try:
            price = float(row[4])
        except:
            return None

        # return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
        return {
            "name": symbol.upper(), # for backward compatibility with Yahoo
            "price": price,
            "symbol": symbol.upper()
        }

    except:
        return None


def usd(value):
    """Formats value as USD."""
    return f"${value:,.2f}"

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

def only_signs(s):
    """checks if string contains only special characters"""

    for character in s:

        if character.isalnum():
            return True

    return False

def split_community_search(s):
    "return list with found community and community to search"

    split_location = s.find("__````@#$!^$@#86afsdc")

    # remove _ and put 2 words in tuple
    return (s[:split_location], s[split_location:].replace("__````@#$!^$@#86afsdc", ""))
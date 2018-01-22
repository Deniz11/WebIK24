from cs50 import SQL
from helpers import valid_id

from imdbpie import Imdb
imdb = Imdb()

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")
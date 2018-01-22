from cs50 import SQL
from helpers import valid_id

from imdbpie import Imdb
imdb = Imdb()

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")

"""
In order to use a class use the following syntax: Classname.function_in_class(required arguments)

So for instance when you want to know hom many members the community ChinaHaters has you can
use the class Communities and use the function members. To do this you would type the following syntax: Communities.member("ChinaHaters")
Keep in mind that it will return an empty list if the community has no members or doesn't exist

note: because the class in application.py is imported as com you need to type com instead of Community so the former syntax would look like this: com.member("ChinaHaters")

"""
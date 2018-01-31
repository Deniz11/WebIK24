from cs50 import SQL
from flask import flash
from helpers import valid_id
from user import User
from search import Search
from user import User

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")


class Lists():


    # create list
    def create_list(owner, listname):
        db.execute("INSERT INTO lists (owner, list_name) VALUES(:owner, :listname)", owner=owner, listname=listname)

    # delete list
    def delete_list(listname):
        db.execute("DELETE FROM lists WHERE id = :id", id=listname)
        db.execute("DELETE FROM list_item WHERE list_id = :list_id", list_id=listname)

    # add item to list
    def add_item(list_id, film_id):
        # insert movie in database if not in database
        if len(db.execute("SELECT * FROM films WHERE film_id = :film_id", film_id=film_id)) == 0:
            db.execute("INSERT INTO films (film_id, title, summary, year, image) VALUES (:film_id, :title, :summary, :year, :image)", film_id = film_id, title = Search.title_name(film_id), summary = Search.title_summary(film_id), year = Search.title_year(film_id), image = Search.title_poster(film_id))

        # add film to list
        if len(db.execute("SELECT * FROM list_item WHERE list_id = :list_id AND film_id = :film_id", film_id = film_id, list_id = list_id)) == 0:
            db.execute("INSERT INTO list_item (list_id, film_id) VALUES (:list_id, :film_id)", list_id=list_id, film_id=film_id)
            return True
        # returnt false if film already in list
        else:
            return False

    # remove item from list
    def remove_item(list_id, film_id):
        db.execute("DELETE FROM list_item WHERE list_id = :list_id AND film_id = :film_id", list_id=list_id, film_id=film_id)

    # get list_id of user/community
    def get_listid(owner):
        return db.execute("SELECT id FROM lists WHERE owner= :owner ", owner = owner)[0]["id"]

    # get list of dics of users film
    def showlist(owner):

        # get list id
        list_id =  Lists.get_listid(owner)

        # return films of user
        if len(db.execute("SELECT film_id FROM list_item WHERE list_id= :list_id", list_id = list_id)) == 0:
            return []
        films = db.execute("SELECT film_id FROM list_item WHERE list_id= :list_id", list_id = list_id)

        films_info = []

        # put movie information from database in list
        for film in films:

            # get movie id from dic
            film_id = film["film_id"]

            # get movie data from database
            film_data =  db.execute("SELECT film_id,title,summary,year,image FROM films WHERE film_id = :film ", film = film_id)[0]

            # add to list
            films_info.append(film_data)

        return films_info

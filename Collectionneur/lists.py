from cs50 import SQL
from flask import flash
from helpers import valid_id
from user import User
from search import Search
from user import User

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")


class Lists():


    # lijst aanmaken
    def create_list(owner, listname):
        db.execute("INSERT INTO lists (owner, list_name) VALUES(:owner, :listname)", owner=owner, listname=listname)
        #return render_template("list.html")


    # lijst verwijderen
    def delete_list(listname):
        db.execute("DELETE FROM lists WHERE id = :id", id=listname)
        db.execute("DELETE FROM list_item WHERE list_id = :list_id", list_id=listname)
        #return redirect(url_for("overzicht"))

    # item aan lijst toevoegen
    def add_item(list_id, film_id):
        # insert movie in database indien nog niet aanwezig
        if len(db.execute("SELECT * FROM films WHERE film_id = :film_id", film_id=film_id)) == 0:
            db.execute("INSERT INTO films (film_id, title, summary, year, image) VALUES (:film_id, :title, :summary, :year, :image)", film_id = film_id, title = Search.title_name(film_id), summary = Search.title_summary(film_id), year = Search.title_year(film_id), image = Search.title_poster(film_id))

        # voeg film toe aan lijst
        if len(db.execute("SELECT * FROM list_item WHERE list_id = :list_id AND film_id = :film_id", film_id = film_id, list_id = list_id)) == 0:
            db.execute("INSERT INTO list_item (list_id, film_id) VALUES (:list_id, :film_id)", list_id=list_id, film_id=film_id)
            flash("Succesfully added to list!")
            return True
        # returnt false als film al in lijst zit
        else:
            flash("Item already in list.")
            return False
       # return redirect(url_for("list"))


    # item verwijderen van lijst
    def remove_item(list_id, film_id):
        db.execute("DELETE FROM list_item WHERE list_id = :list_id AND film_id = :film_id", list_id=list_id, film_id=film_id)
        #return redirect(url_for("list"))

    def get_listid(owner):
        print(owner)
        print(db.execute("SELECT id FROM lists WHERE owner= :owner ", owner = owner)[0]["id"])
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

from cs50 import SQL
from helpers import valid_id
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
    def add_item(name, film):
        list_id = Lists.name_to_id(name)[0]["id"]

        if len(db.execute("SELECT * FROM list_item WHERE list_id = :list_id AND film_id = :film_id", film_id = film, list_id = list_id)) == 0:
            db.execute("INSERT INTO list_item (list_id, film_id) VALUES (:list_id, :film_id)", list_id=list_id, film_id=film)
            return True
        else:
            return False
       # return redirect(url_for("list"))


    # item verwijderen van lijst
    def remove_item(list_id, film_id):
        db.execute("DELETE FROM list_item WHERE list_id = :list_id AND film_id = :film_id", list_id=list_id, film_id=film_id)
        #return redirect(url_for("list"))


    # get user_id from name
    def name_to_id(name):
        return db.execute("SELECT id FROM lists WHERE owner = :name", name = name)

    # get list of dics of users film
    def user_films(id):

        # get username from id
        username = User.get_username(id)

        # get list id
        list_id =  db.execute("SELECT id FROM lists WHERE owner= :username ", username = username)[0]["id"]

        # return films of user
        films = db.execute("SELECT film_id FROM list_item WHERE list_id= :list_id", list_id = list_id)

        films_info = []

        # put movie information from database in list
        for film in films:

            # get movie id from dic
            film_id = film["film_id"]

            # get movie data from database
            film_data =  db.execute("SELECT title,summary,year,image FROM films WHERE film_id = :film ", film = film_id)[0]

            # add to list
            films_info.append(film_data)

        return films_info

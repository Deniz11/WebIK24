from cs50 import SQL
from helpers import valid_id


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
        list_id = Lists.name_to_id(name)
        lijstje = db.execute("SELECT * FROM list_item WHERE film_id = :film", film = film)
        db.execute("INSERT INTO list_item (list_id, film_id) VALUES(:list_id, :film_id)", list_id=list_id, film_id=film)
       # return redirect(url_for("list"))


    # item verwijderen van lijst
    def remove_item(list_id, film_id):
        db.execute("DELETE FROM list_item WHERE list_id = :list_id AND film_id = :film_id", list_id=list_id, film_id=film_id)
        #return redirect(url_for("list"))


    #
    def name_to_id(name):
        return db.execute("SELECT id FROM lists WHERE owner = :name", name = name)

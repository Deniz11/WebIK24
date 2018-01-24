from cs50 import SQL
from user import User
from imdbpie import Imdb
from flask import flash
from flask_session import Session
imdb = Imdb()
from tempfile import mkdtemp

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")



class Communities():

    # Community aanmaken.
    def create(communityname, userid, description):

        users = db.execute("SELECT * FROM users WHERE username = :communityname", communityname=communityname)
        communities = db.execute("SELECT * FROM community_page WHERE name = :communityname", communityname=communityname)

        if len(users) == 1 or len(communities) == 1:
            return flash("name already in use")
        else:
            db.execute("INSERT INTO community_page (name, description) VALUES(:name, :description)", name=communityname, description=description)
            db.execute("INSERT INTO community_users (communityname, username) VALUES(:communityname, :username)", communityname=communityname, username=User.get_username(userid))
            db.execute("INSERT INTO lists (owner, description) VALUES(:owner, :name)", owner=communityname, name=communityname+" Shared List")
            return True

    # Community verwijderen.
    def delete(name):
        db.execute("DELETE FROM community_page WHERE communityname=:communityname", communityname=community)
        db.execute("DELETE FROM community_users WHERE communityname=:communityname", communityname=community)
        #return redirect(url_for("overzicht"))


    # lid worden
    def join(name, community):

        if not db.execute("SELECT * FROM community_users WHERE communityname = :communityname AND username = :username", communityname = community, username = name):
            db.execute("INSERT INTO community_users (communityname , username) VALUES (:communityname, :username)", communityname = community, username = name)
            return True
        else:
            return False

    # Lid verwijderen.
    def remove_member(name, community):
        # CODE TOEVOEGEN VOOR OWNER OF LAATSTE MEMBER
        if not db.execute("SELECT * FROM community_users WHERE communityname = :communityname AND username = :username", communityname = community, username = name):
            return flash("user not in community")
        else:
            db.execute("DELETE FROM community_users WHERE communityname=:communityname AND username=:username", communityname=community, username=name)
            return flash("successfully left community")
        #return redirect(url_for("overzicht"))

    # Return lijst met leden
    def showmembers(communityname):
        rows = db.execute("SELECT username FROM community_users WHERE communityname=:communityname", communityname=communityname)
        return [row["username"] for row in rows]

    # Returnt overzicht van communities.
    def show(communityname = ""):
        # Returnt alle communities indien invoer leeg is.
        if not communityname:
            return db.execute("SELECT * FROM community_page")
        # Zoekt gegevens van specifieke community.
        else:
            return db.execute("SELECT * FROM community_page WHERE name=:communityname",communityname=communityname)

    def all_communities():
        """returns list of all communities"""
        rows = db.execute("SELECT name FROM community_page")
        return [row["name"] for row in rows]

    def mycommunities(userid):
        # Returns alle communities waar gebruiker lid van is
        pages = db.execute("SELECT communityname FROM community_users WHERE username=:username",username=User.get_username(userid))
        return [Communities.show(page["communityname"])[0] for page in pages]

    def member(userid, communityname):
        username = db.execute("SELECT username FROM users WHERE id = :id", id=userid)[0]["username"]
        check = db.execute("SELECT username FROM community_users WHERE communityname = :communityname", communityname=communityname)
        for name in check:
            if username == name["username"]:
                return True
        return False
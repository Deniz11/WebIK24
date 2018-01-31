from cs50 import SQL
from user import User
from imdbpie import Imdb
from flask import flash, session
from flask_session import Session
imdb = Imdb()
from tempfile import mkdtemp

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")

class Communities():

    # Community aanmaken.
    def create(communityname, description):

        users = db.execute("SELECT * FROM users WHERE username = :communityname", communityname=communityname)
        communities = db.execute("SELECT * FROM community_page WHERE name = :communityname", communityname=communityname)

        if len(users) == 1 or len(communities) == 1:
            return flash("name already in use")
        else:
            db.execute("INSERT INTO community_page (name, description) VALUES(:name, :description)", name=communityname, description=description)
            db.execute("INSERT INTO community_users (communityname, username) VALUES(:communityname, :username)", communityname=communityname, username=session["username"])
            db.execute("INSERT INTO lists (owner, list_name) VALUES(:owner, :name)", owner=communityname, name=communityname+" Shared List")
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

    def get_list_id(communityname):
        return db.execute("SELECT * FROM lists WHERE owner = :communityname", communityname=communityname)[0]["id"]

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
            pages = db.execute("SELECT * FROM community_page")

        # Zoekt gegevens van specifieke community.
        else:
            pages = db.execute("SELECT * FROM community_page WHERE LOWER(name)=:communityname",communityname=communityname.lower())

        for page in pages:
            page["members"] = len(Communities.showmembers(page["name"]))
            page["length"] = len(Communities.showlist(Communities.get_list_id(page["name"])))
        return pages

    def mycommunities():
        # Returns alle communities waar gebruiker lid van is
        pages = db.execute("SELECT communityname FROM community_users WHERE username=:username",username=session["username"])
        return [Communities.show(page["communityname"])[0] for page in pages]

    def member(userid, communityname):
        check = db.execute("SELECT username FROM community_users WHERE communityname = :communityname", communityname=communityname)
        for name in check:
            if session["username"] == name["username"]:
                return True
        return False

    def showlist(list_id):
        # returns a single communitylist
        return db.execute("SELECT film_id FROM list_item WHERE list_id = :list_id", list_id=list_id)

    def save_comment(username, community, comment):
        return db.execute("INSERT INTO comment_section (community, username, comment) VALUES(:community, :username, :comment)", community = community, username = username, comment=comment)

    def community_comments(community):
        return db.execute("SELECT username,datetime,comment FROM comment_section WHERE community = :community ORDER BY datetime(datetime) DESC", community=community)

    def change_description(new_description, community):
        return db.execute("UPDATE community_page SET description = :new_description WHERE name = :community", community = community, new_description = new_description)
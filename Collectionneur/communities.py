from cs50 import SQL

from imdbpie import Imdb
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
            return False
        else:
            username = db.execute("SELECT username FROM users WHERE id = :id", id=userid)[0]["username"]
            db.execute("INSERT INTO community_page (name, description) VALUES(:name, :description)", name=communityname, description=description)
            db.execute("INSERT INTO community_users (communityname, username) VALUES(:communityname, :username)", communityname=communityname, username=username)
            db.execute("INSERT INTO lists (owner, description) VALUES(:owner, :name)", owner=communityname, name=communityname+" Shared List")

    # Community verwijderen.
    def delete(name):
        db.execute("DELETE FROM community_page WHERE communityname=:communityname", communityname=community)
        db.execute("DELETE FROM community_users WHERE communityname=:communityname", communityname=community)
        #return redirect(url_for("overzicht"))

    # Lid worden.
    def join(name):

        db.execute("INSERT INTO community_users WHERE username=:username", username=name)
        #return redirect(url_for("community"))

    # Lid verwijderen.
    def remove(community, name):
        db.execute("DELETE FROM community_users WHERE communityname=:communityname AND username=:username", communityname=community, username=name)
        #return redirect(url_for("overzicht"))

    # Return lijst met leden
    def members(communityname):
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

    def mycommunities(user_id):
        # Returns alle communities waar gebruiker lid van is
        username = db.execute("SELECT username FROM users WHERE id = :id", id=user_id)[0]["username"]
        pages = db.execute("SELECT communityname FROM community_users WHERE username=:username",username=username)
        print(pages)
        test = [Communities.show(page["communityname"])[0] for page in pages]
        print(test)
        return test
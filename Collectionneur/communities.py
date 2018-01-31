from cs50 import SQL
from user import User
from lists import Lists
from imdbpie import Imdb
from flask import flash, session
from flask_session import Session
imdb = Imdb()
from tempfile import mkdtemp

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")



class Communities():

    # Create community.
    def create(communityname, description):

        # Get data from database.
        users = db.execute("SELECT * FROM users WHERE username = :communityname", communityname=communityname)
        communities = db.execute("SELECT * FROM community_page WHERE name = :communityname", communityname=communityname)
        # Check if community already exists
        if len(users) == 1 or len(communities) == 1:
            return
        # Add community to database.
        else:
            db.execute("INSERT INTO community_page (name, description) VALUES(:name, :description)", name=communityname, description=description)
            db.execute("INSERT INTO community_users (communityname, username) VALUES(:communityname, :username)", communityname=communityname, username=session["username"])
            db.execute("INSERT INTO lists (owner, list_name) VALUES(:owner, :name)", owner=communityname, name=communityname+" Shared List")
            return True

    # Delete community.
    def delete(name):
        # Delete community from database.
        db.execute("DELETE FROM community_page WHERE communityname=:communityname", communityname=community)
        db.execute("DELETE FROM community_users WHERE communityname=:communityname", communityname=community)


    # Join community.
    def join(name, community):
        # Returns true on succes.
        if not db.execute("SELECT * FROM community_users WHERE communityname = :communityname AND username = :username", communityname = community, username = name):
            db.execute("INSERT INTO community_users (communityname , username) VALUES (:communityname, :username)", communityname = community, username = name)
            return True
        # Returns false if user already in community.
        else:
            return False

    # Get community list id.
    def get_list_id(communityname):
        return db.execute("SELECT * FROM lists WHERE owner = :communityname", communityname=communityname)[0]["id"]

    # Remove member.
    def remove_member(name, community):

        # Check if user is member.
        if not db.execute("SELECT * FROM community_users WHERE communityname = :communityname AND username = :username", communityname = community, username = name):
            return

        # Remove member from community.
        else:
            db.execute("DELETE FROM community_users WHERE communityname=:communityname AND username=:username", communityname=community, username=name)
            return

    # Return memberlist.
    def showmembers(communityname):

        # Returns list of all the members.
        rows = db.execute("SELECT username FROM community_users WHERE communityname=:communityname", communityname=communityname)
        return [row["username"] for row in rows]

    # Returns overview for communities
    def show(communityname = ""):

        # Returns ALL communities if no parameter is given.
        if not communityname:
            pages = db.execute("SELECT * FROM community_page")

        # Returns all information for a specific community.
        else:
            pages = db.execute("SELECT * FROM community_page WHERE LOWER(name)=:communityname",communityname=communityname.lower())

        # Add amount of members and items
        for page in pages:
            page["members"] = len(Communities.showmembers(page["name"]))
            page["length"] = len(Communities.showlist(Communities.get_list_id(page["name"])))
        return pages

    # Return my communities.
    def mycommunities():

        # Returns all communities the usere is a member of.
        pages = db.execute("SELECT communityname FROM community_users WHERE username=:username",username=session["username"])
        return [Communities.show(page["communityname"])[0] for page in pages]

    # Check if someone is a member.
    def member(userid, communityname):
        check = db.execute("SELECT username FROM community_users WHERE communityname = :communityname", communityname=communityname)

        # If user in community return true
        for name in check:
            if session["username"] == name["username"]:
                return True
        # Return false if user not a member.
        return False

    # Returns communitylist.
    def showlist(list_id):
        # returns a single communitylist
        return db.execute("SELECT film_id FROM list_item WHERE list_id = :list_id", list_id=list_id)

    # Save comment to database.
    def save_comment(username, community, comment):
        return db.execute("INSERT INTO comment_section (community, username, comment) VALUES(:community, :username, :comment)", community = community, username = username, comment=comment)

    # Return comments.
    def community_comments(community):
        return db.execute("SELECT username,datetime,comment FROM comment_section WHERE community = :community ORDER BY datetime(datetime) DESC", community=community)

    # change description
    def change_description(new_description, community):
        return db.execute("UPDATE community_page SET description = :new_description WHERE name = :community", community = community, new_description = new_description)

    # Generate a list preview for search results.
    def preview(communityname):
        comlist = Lists.showlist(communityname)
        preview = [film["image"] for film in comlist][:4]

        # Add stock photo's if list is too short.
        while len(preview) < 4:
            preview.append("https://cdn2.iconfinder.com/data/icons/cinema-and-television/500/Entertainment_film_film_reel_film_roll_movie_reel_roll_theate-512.png")
        return preview


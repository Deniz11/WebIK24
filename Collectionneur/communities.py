from cs50 import SQL

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")

"""
In order to use a class use the following syntax: Classname.function_in_class(required arguments)

So for instance when you want to know hom many members the community ChinaHaters has you can
use the class Communities and use the function members. To do this you would type the following syntax: Communities.member("ChinaHaters")
Keep in mind that it will return an empty list if the community has no members or doesn't exist

note: because the class in application.py is imported as com you need to type com instead of Community so the former syntax would look like this: com.member("ChinaHaters")

"""

class Communities():

    # Community aanmaken.
    def create(community, user, summary):
        db.execute("INSERT INTO community_page (username, description) VALUES(:username, :description)", username=user, description=summary)
        db.execute("INSERT INTO community_users (communityname, username) VALUES(:communityname, :username)", communityname=community, username=user)
        return render_template(community.html)

    # Community verwijderen.
    def delete(name):
        db.execute("DELETE FROM community_page WHERE communityname=:communityname", communityname=community)
        db.execute("DELETE FROM community_users WHERE communityname=:communityname", communityname=community)
        return redirect(url_for("overzicht"))

    # Lid worden.
    def join(name):
        db.execute("INSERT INTO community_users WHERE username=:username", username=name)
        return redirect(url_for("community"))

    # Lid verwijderen.
    def remove(community, name):
        db.execute("DELETE FROM community_users WHERE communityname=:communityname AND username=:username", communityname=community, username=name)
        return redirect(url_for("overzicht"))

    # Return lijst met leden
    def members(name):
        rows = db.execute("SELECT username FROM community_users WHERE communityname=:communityname", communityname=name)
        return [row["username"] for row in rows]
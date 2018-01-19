class Communities():

    # Community aanmaken.
    def create(self):

        return render_template(community.html)

    # Community verwijderen.
    def delete(self, name):
        db.execute("DELETE FROM community_page WHERE communityname=:communityname", communityname=community)
        db.execute("DELETE FROM community_users WHERE communityname=:communityname", communityname=community)
        return redirect(url_for("overzicht"))

    # Lid worden.
    def join(self, name):
        db.execute("INSERT INTO community_users WHERE username=:username", username=name)
        return redirect(url_for("overzicht"))

    # Lid verwijderen.
    def remove(self, community, name):
        db.execute("DELETE FROM community_users WHERE communityname=:communityname AND username=:username", communityname=community, username=name)
        return redirect(url_for("overzicht"))

    # Return lijst met leden
    def members(self, name):
        rows = db.execute("SELECT username FROM community_users WHERE communityname=:communityname", communityname=name)
        return [row["username"] for row in rows]
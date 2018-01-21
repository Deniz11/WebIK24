from cs50 import SQL

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")

''' User class '''

class User():
    def __init__(self, username, password):
        self.username = username

    def registeruser():
        # register user
        hash1 = pwd_context.hash(request.form.get("password"))
        rows=db.execute("INSERT INTO users (username, hash) VALUES(:username, :password)", username=request.form.get("username"), password=hash1)
        # let user log in
        flash("Account succesfully created")
        return redirect(url_for("login"))

    def changepass():
        # update password
        db.execute("UPDATE users SET hash = :hash1 WHERE id= :id ",hash1 = hash1, id = session["user_id"])
        # show index page
        flash("Succesfully changed password")
        return redirect(url_for("index"))

    def deleteaccount():
        # delete user
        db.execute("DELETE FROM users WHERE id= :id ", id = session["user_id"])
        # show index/log in page
        flash("Succesfully deleted account")
        return redirect(url_for("logout"))
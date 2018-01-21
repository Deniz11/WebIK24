from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
# from communities import communities as com
from communities import Communities as com

from imdbpie import Imdb
imdb = Imdb()

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")

@app.route("/")
@login_required
def index():
    popular = imdb.get_popular_titles()
    return render_template("index.html", popular=popular)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    #session.clear()


    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            flash("Please provide an username")
            return render_template("login.html")

        # ensure password was submitted
        elif not request.form.get("password"):
            flash("Please provide a password")
            return render_template("login.html")

        # for test purposes
        print(test(request.form.get("username")))

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            flash("Invalid username and/or password")
            return render_template("login.html")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        flash("succesfully logged in")
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    flash("You have succesfully logged out")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
     # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            flash("Please provide an username")
            return render_template("register.html")

        # ensure password was submitted
        elif not request.form.get("password") and not request.form.get("password-again"):
            flash("Please provide a password")
            return render_template("register.html")

        elif request.form.get("password") != request.form.get("password-again"):
            flash("Passwords do not match!")
            return render_template("register.html")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists
        if len(rows) == 1:
            flash("Seems like this username already exists, please provide another one.")
            return render_template("register.html")

        # register user
        hash1 = pwd_context.hash(request.form.get("password"))
        rows=db.execute("INSERT INTO users (username, hash) VALUES(:username, :password)", username=request.form.get("username"), password=hash1)


        # let user log in
        flash("Account succesfully created")
        return redirect(url_for("login"))

    else:
        return render_template("register.html")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Settings."""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if request.form.get("change password selected"):

            # ensure password was submitted
            if not request.form.get("password"):
                flash("Please fill in your current password")
                return render_template("settings.html")

            # ensure new password was submitted
            if not request.form.get("password-new"):
                flash("Please fill in your new password")
                return render_template("settings.html")

            # ensure new password was submitted again
            if not request.form.get("password-new-again"):
                flash("Please fill in your new password again")
                return render_template("settings.html")

            # ensure new password matches
            if not request.form.get("password-new") == request.form.get("password-new-again"):
                flash("New passwords do not match")
                return render_template("settings.html")

            # query database for password
            rows = db.execute("SELECT hash FROM users WHERE id = :id", id = session["user_id"])

            ##print(rows[0]["hash"])

            # hash password
            hash2 = pwd_context.hash(request.form.get("password"))

            # ensure that password is correct
            if not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
                flash("Incorrect password")
                return render_template("settings.html")

            # hash new password
            hash1 = pwd_context.hash(request.form.get("password-new"))

            # update password
            db.execute("UPDATE users SET hash = :hash1 WHERE id= :id ",hash1 = hash1, id = session["user_id"])

            # show index page
            flash("Succesfully changed password")
            return redirect(url_for("index"))

        if request.form.get("delete account selected"):

            # ensure password was submitted
            if not request.form.get("username"):
                flash("Please fill in your current username")
                return render_template("settings.html")

            # ensure password was submitted
            if not request.form.get("password") or not request.form.get("password-again"):
                flash("Please fill in your password")
                return render_template("settings.html")

            if request.form.get("password") != request.form.get("password-again"):
                flash("Passwords do not match!")
                return render_template("settings.html")

            # query database for password
            rows = db.execute("SELECT hash FROM users WHERE id = :id", id = session["user_id"])

            # ensure that password is correct
            if not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
                flash("Incorrect password")
                return render_template("settings.html")

            if not request.form.get("delete account"):
                flash("Please verify that you want to delete your account!")
                return render_template("settings.html")

            # delete user
            db.execute("DELETE FROM users WHERE id= :id ", id = session["user_id"])

            # show index/log in page
            flash("Succesfully deleted account")
            return redirect(url_for("logout"))

        else:
            flash("nothing selected")
            return render_template("settings.html")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("settings.html")

@app.route("/createcommunity", methods=["GET", "POST"])
@login_required
def createcommunity():

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # pass input to function
        com.create(request.form.get("communityname"), request.form.get("communitydescription"))

        # redirect to newly created community
        return redirect(url_for("community"))

    else:
        return render_template("createcommunity.html")
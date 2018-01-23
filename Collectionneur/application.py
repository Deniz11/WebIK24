from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from communities import Communities as com
from user import User
from homepage import Home as home
from search import Search

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
    ranks = home.get_popular_movies()
    # lists = User.mylists()
    return render_template("index.html", ranks=ranks)

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
        username=request.form.get("username")
        # query database for username
        rows = User.userexist(username)

        # ensure username exists and password is correct
        if not User.userexist(username) or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
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


        # ensure username exists
        if not User.userexist(username):
            flash("Seems like this username already exists, please provide another one.")
            return render_template("register.html")

        # register user
        hash1 = pwd_context.hash(request.form.get("password"))
        User.registeruser(username, hash1)

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
            id = session["user_id"]
            rows = User.requestpassword(id)

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
            User.changepassword(hash1, id)

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
            id = session["user_id"]
            rows = User.requestpassword(id)

            # ensure that password is correct
            if not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
                flash("Incorrect password")
                return render_template("settings.html")

            if not request.form.get("delete account"):
                flash("Please verify that you want to delete your account!")
                return render_template("settings.html")

            # delete user
            User.deleteaccount(id)

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
         if not com.create(request.form.get("communityname"), session["user_id"], request.form.get("communitydescription")):
             flash("name already in use")

        # redirect to newly created community
        return redirect(url_for("community", name=request.form.get("communityname")))

    else:
        return render_template("createcommunity.html")

@app.route("/community", methods=["GET", "POST"])
@login_required
def community():
    return render_template("community.html", name=request.args.get('name'))

@app.route("/communityoverview", methods=["GET", "POST"])
@login_required
def communityoverview():# GEEFT OVERVIEW WEER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<DEZE LATER IN TOTAALOVERZICHT ZETTEN!!!!!!!!!!!!!!!!!!!!!
    overview = com.show("")
    return render_template("communityoverview.html", overview=overview)

@app.route("/search", methods=["GET", "POST"])
def search():

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # check if user want to join community
        if request.form.get("join community"):

            # get community to join and to search
            split = split_community_search(request.form.get("join community"))

            # join community

            # search communities
            communities_found = Search.community(split[1])

            return render_template("search.html", communities_found = communities_found, to_search = ("__````@#$!^$@#86afsdc" + split[1]), community_select = True)

        # go to community page
        if request.form.get("go to community page"):
            flash("todo go to community page")
            return render_template("search.html")

        # check if more information route clicked
        if request.form.get("imdb_id"):

            full_movie_info = Search.title_info(request.form.get("imdb_id"))

            return render_template("movie_information.html", full_movie_info = full_movie_info, movie_select = True)

        # check if user want to add item to list
        if request.form.get("add_to_list"):

            # check if something filled in
            if not request.form.get("name"):
                full_movie_info = Search.title_info(request.form.get("add_to_list"))
                flash("please fill in a community/user")
                return render_template("movie_information.html", full_movie_info = full_movie_info, movie_select = True)

            # add list to community user

            # add film in films
            Search.add_item(request.form.get("add_to_list"))

            full_movie_info = Search.title_info(request.form.get("add_to_list"))
            return render_template("movie_information.html", full_movie_info = full_movie_info, movie_select = True)


        # if nothing selected to search for
        if request.form.get("search_for") == "None":
            flash("please select something to search")
            return render_template("search.html", select_something_select = True)

        # if movie selected to search for
        if request.form.get("search_for") == "movie":

            # check if something filled in
            if not request.form.get("search"):
                flash("please fill in something to search")
                return render_template("search.html", movie_select = True)

            # check if something found or valid search given
            if not only_signs(request.form.get("search")) or not Search.search_titles(request.form.get("search")):
                flash("Nothing found")
                return render_template("search.html", movie_select = True)

            all_movie_info = Search.search_titles(request.form.get("search"))
            return render_template("search.html", all_movie_info=all_movie_info, movie_select = True)


        # if community selected to search for
        if request.form.get("search_for") == "community":

            # remember search name
            to_search = request.form.get("search")

            # check if something filled in
            if not to_search:
                flash("please fill in something to search")
                return render_template("search.html", community_select = True)

            # search communities
            communities_found = Search.community(to_search)

            # notify that no communities similiar to search
            if not communities_found:
                flash("no communities found")
                render_template("search.html", community_select = True)

            return render_template("search.html", communities_found = communities_found, to_search = ("__````@#$!^$@#86afsdc" + request.form.get("search")), movie_select = True)


    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("search.html")
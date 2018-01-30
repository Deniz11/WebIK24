from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from communities import Communities as com
from user import User
from homepage import Home as home
from search import Search
from lists import Lists

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
def index():
    try:
        session["user_id"]
        username=session["username"]
    except KeyError:
        username = ""
    movies = home.get_popular_movies()
    print(movies)

    #print(movies)
    return render_template("index.html", movies=movies, pages=home.rank_communities(), username=username)

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

        # ensure username exists and password is correct
        if not User.user(request.form.get("username")) or not pwd_context.verify(request.form.get("password"), User.user(request.form.get("username"))[0]["hash"]):
            flash("Invalid username and/or password")
            return render_template("login.html")

        # remember which user has logged in
        session["user_id"] = User.user(request.form.get("username"))[0]["id"]
        session["username"] = request.form.get("username")

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
        if User.userexist(request.form.get("username")):
            flash("Seems like this username already exists, please provide another one.")
            return render_template("register.html")

        # register user
        hash1 = pwd_context.hash(request.form.get("password"))
        User.registeruser(request.form.get("username"), hash1)

        # make list name
        list_name = "list of " + request.form.get("username")

        # give an user a list
        Lists.create_list(request.form.get("username"), list_name)

        # let user log in
        flash("Account succesfully created")

        # remember which user has logged in
        session["user_id"] = User.user(request.form.get("username"))[0]["id"]
        session["username"] = request.form.get("username")

        # redirect user to home page
        return redirect(url_for("index"))

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
            User.deleteaccount(session["username"])

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
        if com.create(request.form.get("communityname"), request.form.get("communitydescription")):
            # redirect to newly created community
            return redirect(url_for("community", community=request.form.get("communityname")))

        return render_template("createcommunity.html")
    else:
        return render_template("createcommunity.html")



@app.route("/community", methods=["GET", "POST"])
@login_required
def community():

    # add random films for TEST PURPOSES
    films = Lists.showlist(request.args.get('community'))
    comments = com.community_comments(request.args.get('community'))

    if request.method == "POST":

        if request.form.get("commented"):
            username = session["username"]
            com.save_comment(username, request.args.get('community'), request.form.get("comment"))
            comments = com.community_comments(request.args.get('community'))
            return render_template("community.html", comments = comments, page=com.show(request.args.get('community'))[0], members=com.showmembers(request.args.get('community')), films=films, member=com.member(session["user_id"], request.args.get('community')))

        if request.form.get("comaction") == "join":

            com.join(session["username"] ,request.args.get('community'))

            return render_template("community.html", comments = comments, page=com.show(request.args.get('community'))[0], members=com.showmembers(request.args.get('community')), films=films, member=com.member(session["user_id"], request.args.get('community')))

        elif request.form.get("comaction") == "leave":

            com.remove_member(session["username"],request.args.get('community'))

            return render_template("community.html", comments = comments, page=com.show(request.args.get('community'))[0], members=com.showmembers(request.args.get('community')), films=films, member=com.member(session["user_id"], request.args.get('community')))

        #wrong post request
        else:
            return render_template("community.html", comments = comments, page=com.show(request.args.get('community'))[0], members=com.showmembers(request.args.get('community')), films=films, member=com.member(session["user_id"], request.args.get('community')))

    else:

        return render_template("community.html" ,comments = comments, page=com.show(request.args.get('community'))[0], members=com.showmembers(request.args.get('community')), films=films, member=com.member(session["user_id"], request.args.get('community')))

@app.route("/communityoverview", methods=["GET", "POST"])

def communityoverview():# GEEFT OVERVIEW WEER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<DEZE LATER IN TOTAALOVERZICHT ZETTEN!!!!!!!!!!!!!!!!!!!!!
    print(com.show())
    return render_template("communityoverview.html", overview=com.show())

@app.route("/mycommunities", methods=["GET", "POST"])
@login_required

def mycommunities():
    return render_template("mycommunities.html", pages=com.mycommunities(session["user_id"]))

@app.route("/actor_info", methods=["GET", "POST"])
def actor_info():

    actors_information = Search.actor_information(request.args.get("actor_id"))
    recent_movies = Search.actor_movies(request.args.get("actor_id"))

    return render_template("actor_information.html", actor = actors_information, recent_movies = recent_movies, actor_select = True)

@app.route("/movie_info", methods=["GET", "POST"])
def movie_info():


    print(request.args.get("imdb_id"))
    try:
        session["user_id"]
        mycommunities = com.mycommunities(session["user_id"])
    except KeyError:
        mycommunities = []

    similar_films = Search.similar_films(request.args.get("imdb_id"))
    actors = Search.movie_actors(request.args.get("imdb_id"))
    full_movie_info = Search.title_info(request.args.get("imdb_id"))

    if request.method == "POST":
        if request.form.get("listadd") == "add":
            Lists.add_item(User.get_list_id(session["username"]), request.args.get("imdb_id"))
            return render_template("movie_information.html", full_movie_info = full_movie_info, actors = actors, similars = similar_films, movie_select = True, mycom=mycommunities)
        else:
            Lists.add_item(com.get_list_id(request.form.get("comadd")), request.args.get("imdb_id"))
            return render_template("movie_information.html", full_movie_info = full_movie_info, actors = actors, similars = similar_films, movie_select = True, mycom=mycommunities)
    else:
        return render_template("movie_information.html", full_movie_info = full_movie_info, actors = actors, similars = similar_films, movie_select = True, mycom=mycommunities)


@app.route("/search", methods=["GET", "POST"])
def search():

    # check if user want to go to community page
    if request.form.get("go to community page"):

        return redirect(url_for('community', community=request.form.get("go to community page")))

    # check if user want to join community
    if request.form.get("join community"):

        # get community to join and to search
        split = split_community_search(request.form.get("join community"))

        # search communities
        communities_found = Search.community(split[1])

        # check if user is logged in
        if "user_id" not in session:
            flash("To use this function, please log in")
            return render_template("search.html", communities_found = communities_found, to_search = ("__````@#$!^$@#86afsdc" + split[1]), community_select = True)

        # join community and if already joined notify user
        if not com.join(session["username"], split[0]):
            flash("you are already a member of this community")
            return render_template("search.html", communities_found = communities_found, to_search = ("__````@#$!^$@#86afsdc" + split[1]), community_select = True)

        flash("succesfully joined community")
        return render_template("search.html", communities_found = communities_found, to_search = ("__````@#$!^$@#86afsdc" + split[1]), community_select = True)

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

        # check if valid search given
        if not only_signs(request.form.get("search")):
            flash("Invalid search, search contains only special characters")
            return render_template("search.html", movie_select = True)

        all_movie_info = Search.search_titles(request.form.get("search"))

        # check if something found
        if not all_movie_info:
            flash("Nothing found")
            return render_template("search.html", movie_select = True)

        return render_template("search.html", all_movie_info=all_movie_info, movie_select = True)

    # if actor selected to search for
    if request.form.get("search_for") == "actor":

        # remember search name
        to_search = request.form.get("search")

        # check if something filled in
        if not to_search:
            flash("please fill in something to search")
            return render_template("search.html", actor_select = True)

        # check if valid search given
        if not only_signs(request.form.get("search")):
            flash("Invalid search, search contains only special characters")
            return render_template("search.html", actor_select = True)

        # search actors
        actors_information = Search.search_actor(to_search)

        # notify that no actors are found
        if not Search.search_actor(to_search):
            flash("Did not find any actors")
            render_template("search.html", community_select = True)

        return render_template("search.html", actors = actors_information, actor_select = True)


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

        return render_template("search.html", communities_found = communities_found, to_search = ("__````@#$!^$@#86afsdc" + request.form.get("search")), community_select = True)

    return render_template("search.html")


@app.route("/mylist", methods=["GET", "POST"])
@login_required
def mylist():

    information = Lists.showlist(session["username"])

    return render_template("lists.html", information=information)

@app.route("/search1", methods=["GET", "POST"])
def search1():
    goal = request.args.get('type')
    query = request.args.get('q')

    if goal == "none":
        flash("Please specify search type")
        return render_template("search1.html")
    if goal == "movie":
        flash([row["imdb_id"] for row in imdb.search_for_title(query) if row["imdb_id"][0] == "t"])
        return render_template("search1.html")
    else:
        flash(com.show(query))
        return render_template("search1.html")

    return render_template("search1.html")





@app.route("/myprofile", methods=["GET", "POST"])
@login_required
def myprofile():

    return render_template("profilepage.html", movies=Lists.showlist(session["username"]), communities=com.mycommunities(session["user_id"]))



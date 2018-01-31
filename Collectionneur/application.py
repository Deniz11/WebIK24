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

    #print(movies)s
    return render_template("index.html", movies=movies, pages=home.rank_communities(), username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username exists and password is correct
        if not User.user(request.form.get("username")) or not pwd_context.verify(request.form.get("password"), User.user(request.form.get("username"))[0]["hash"]):
            return render_template("login.html", InvalidUserMatch = True)

        # remember which user has logged in
        session["user_id"] = User.user(request.form.get("username"))[0]["id"]
        session["username"] = request.form.get("username")

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", InvalidUserMatch = False)

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    flash("You have succesfully logged out")
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username exists
        if User.userexist(request.form.get("username")):
            return render_template("register.html", InUse = True)

        # register user
        hash1 = pwd_context.hash(request.form.get("password"))
        User.registeruser(request.form.get("username"), hash1)

        # make list name
        list_name = "list of " + request.form.get("username")

        # give an user a list
        Lists.create_list(request.form.get("username"), list_name)

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

            # query database for password
            id = session["user_id"]
            rows = User.requestpassword(id)

            # hash password
            hash2 = pwd_context.hash(request.form.get("password"))

            # ensure that password is correct
            if not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
                return render_template("settings.html", OldPasswordIncorrect = True)

            # hash new password
            hash1 = pwd_context.hash(request.form.get("password-new"))

            # update password
            User.changepassword(hash1, id)

            # show index page
            return redirect(url_for("index"))

        if request.form.get("delete account selected"):

            # query database for password
            id = session["user_id"]
            rows = User.requestpassword(id)

            # ensure that user is only deleting his account
            if not (request.form.get("username") == session["username"]):
                return render_template("settings.html", NotCorrectUser=True)

            # ensure that password is correct
            if not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
                return render_template("settings.html", Passwordincorrect = True)

            # delete user
            User.deleteaccount(session["username"])

            # show index/log in page
            return redirect(url_for("logout"))

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

    films = Lists.showlist(request.args.get('community'))
    comments = com.community_comments(request.args.get('community'))

    if request.method == "POST":

        if request.form.get("comaction") == "join":

            com.join(session["username"] ,request.args.get('community'))

            return render_template("community.html", mycom = com.mycommunities(), comments = comments, page=com.show(request.args.get('community'))[0], members=com.showmembers(request.args.get('community')), films=films, member=com.member(session["user_id"], request.args.get('community')))

        elif request.form.get("comaction") == "leave":

            com.remove_member(session["username"],request.args.get('community'))

            return render_template("community.html", mycom = com.mycommunities(), comments = comments, page=com.show(request.args.get('community'))[0], members=com.showmembers(request.args.get('community')), films=films, member=com.member(session["user_id"], request.args.get('community')))

        elif request.form.get("comlistremove"):
            Lists.remove_item(Lists.get_listid(request.args.get('community')), request.form.get("comlistremove"))
            films = Lists.showlist(request.args.get('community'))
            return render_template("community.html", mycom = com.mycommunities(), comments = comments, page=com.show(request.args.get('community'))[0], members=com.showmembers(request.args.get('community')), films=films, member=com.member(session["user_id"], request.args.get('community')))

        if request.form.get("listadd") != 0:
            Lists.add_item(User.get_list_id(session["username"]), request.form.get("listadd"))
            return render_template("community.html" , mycom = com.mycommunities(), comments = comments, page=com.show(request.args.get('community'))[0], members=com.showmembers(request.args.get('community')), films=films, member=com.member(session["user_id"], request.args.get('community')))
        elif request.form.get("comadd") != 0:
            Lists.add_item(com.get_list_id(request.form.get("comadd")), request.form.get("comadd"))
            return render_template("community.html" , mycom = com.mycommunities(), comments = comments, page=com.show(request.args.get('community'))[0], members=com.showmembers(request.args.get('community')), films=films, member=com.member(session["user_id"], request.args.get('community')))

        if request.form.get("commented"):
            username = session["username"]
            com.save_comment(username, request.args.get('community'), request.form.get("comment"))
            comments = com.community_comments(request.args.get('community'))
            return render_template("community.html", mycom = com.mycommunities(), comments = comments, page=com.show(request.args.get('community'))[0], members=com.showmembers(request.args.get('community')), films=films, member=com.member(session["user_id"], request.args.get('community')))



        #wrong post request
        else:
            return render_template("community.html", mycom = com.mycommunities(), comments = comments, page=com.show(request.args.get('community'))[0], members=com.showmembers(request.args.get('community')), films=films, member=com.member(session["user_id"], request.args.get('community')))

    else:

        return render_template("community.html" , mycom = com.mycommunities(), comments = comments, page=com.show(request.args.get('community'))[0], members=com.showmembers(request.args.get('community')), films=films, member=com.member(session["user_id"], request.args.get('community')))

@app.route("/communityoverview", methods=["GET", "POST"])

def communityoverview():
    overview=com.show()
    try:
        session["user_id"]
        username=session["username"]
    except KeyError:
        for item in overview:
            item["member"] = False
        return render_template("communityoverview.html", overview=overview)

    for item in overview:
        if session["username"] in com.showmembers(item["name"]):
            item["member"] = True
        else:
            item["member"] = False

    return render_template("communityoverview.html", overview=overview)

@app.route("/mycommunities", methods=["GET", "POST"])
@login_required

def mycommunities():
    if request.form.get("comaction"):
        com.remove_member(session["username"], request.form.get("comaction"))
    return render_template("mycommunities.html", pages=com.mycommunities())

@app.route("/actor_info", methods=["GET", "POST"])
def actor_info():

    actors_information = Search.actor_information(request.args.get("actor_id"))
    recent_movies = Search.actor_movies(request.args.get("actor_id"))

    return render_template("actor_information.html", actor = actors_information, recent_movies = recent_movies, actor_select = True)

@app.route("/movie_info", methods=["GET", "POST"])
def movie_info():


    try:
        session["user_id"]
        mycommunities = com.mycommunities()
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

    if request.method == "POST":

        Lists.remove_item(Lists.get_listid(session["username"]), request.form.get("listremove"))

    information = Lists.showlist(session["username"])

    return render_template("lists.html", information=information)





@app.route("/myprofile", methods=["GET", "POST"])
@login_required
def myprofile():

    return render_template("profilepage.html", movies=Lists.showlist(session["username"]), communities=com.mycommunities())



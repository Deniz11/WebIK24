from cs50 import SQL
from helpers import valid_id

from imdbpie import Imdb
imdb = Imdb()

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Collectionneur.db")

class Search():

    def search_titles(to_search):
        """return list of dics with searched title and info"""

        # request title, year, imdb_id in dictionary
        title_results = imdb.search_for_title(to_search)

        all_movie_info = []

        # put title, image, year and short discription in list
        for i in range(len(title_results)):

            movie_info = {}

            # look for information in database
            info_database = db.execute("SELECT * FROM films WHERE film_id = :film_id", film_id = title_results[i]["imdb_id"])
            if info_database:

                info_database_indexed = info_database[0]

                # put movie imdb_id in list
                movie_info["imdb_id"] = info_database_indexed["film_id"]

                # put movie title in list
                movie_info["title"] = info_database_indexed["title"]

                # put movie year in list
                movie_info["year"] = info_database_indexed["summary"]

                # put movie image in list
                movie_info["image"] = info_database_indexed["year"]

                #put short plot in list
                movie_info["short plot"] = info_database_indexed["image"]

            # do if imdb_id exist
            if valid_id(title_results[i]["imdb_id"]):

                title_info = imdb.get_title(title_results[i]["imdb_id"])

                # put movie imdb_id in list
                movie_info["imdb_id"] = title_results[i]["imdb_id"]

                # put movie title in list
                movie_info["title"] = title_results[i]["title"]

                # try to find year in searched dic
                try:
                    # put movie year in list
                    movie_info["year"] = title_results[i]["year"]

                    # change none to could not find
                    if movie_info["year"] == None:
                        movie_info["year"] = "Sorry, no year found!"
                except:
                    # try to find year from other dic
                    try:
                        movie_info["year"] = Search.title_year(title_results[i]["imdb_id"])
                    # put notification that nothings is found in dic
                    except:
                        movie_info["year"] = "Sorry, no year found!"

                try:
                    # put a movie image in the list
                    movie_info["image"] = title_info["base"]["image"]['url']
                except:
                    # try to find related image else put image not found image in dic
                    movie_info["image"] = Search.title_poster(title_results[i]["imdb_id"], check = 1)

                # try to find a short plot
                try:
                    # put short plot in dic
                    movie_info["short plot"] = title_info["plot"]["outline"]["text"]
                except:
                    # try to find a summary
                    try:
                        # put summary in dic
                        movie_info["short plot"] = Search.title_summary(title_results[i]["imdb_id"])
                    except:
                        # put in dic a notification that nothing is found
                        movie_info["short plot"] = "Sorry, no plot found!"

                # put the movie_info in a list
                all_movie_info.append(movie_info)

        return all_movie_info

    def title_info(imdb_id):
        """Returns list of dics of all possible title info"""

        # check if valid imdb_id
        if valid_id(imdb_id):

            full_movie_info = {}

            # get title information
            title_info_id = imdb.get_title(imdb_id)

            # put imdb_id in in dic
            full_movie_info["imdb_id"] = imdb_id

            # put movie title in dic
            full_movie_info["title"] = title_info_id["base"]['title']

            # try to put movie year in dic
            try:
                full_movie_info["year"] = title_info_id["base"]['year']
            except:
                full_movie_info["year"] = "Sorry, no year found!"

            # try to put a movie image in the dic
            full_movie_info["image"] = Search.title_poster(imdb_id)

            # if there are no summaries put outline in dic
            full_movie_info["plot"] = Search.title_summary(imdb_id)

            # try to get genre list
            try:
                genres = imdb.get_title_genres(imdb_id)["genres"]

                s = ''

                # turn list in string
                for genre in genres:

                    if not s:
                        s = s + genre

                    else:
                        s = s + ", " + genre

                # put movie genre(s) in dic
                full_movie_info["genre"] = s

            except:
                full_movie_info["genre"] = "nothing found"

            # try to get movie rating
            try:
                full_movie_info["rating"] = imdb.get_title_ratings(imdb_id)["rating"]
            except:
                full_movie_info["rating"] = "no ratings found"

            return full_movie_info

        else:
            return False

    def title_name(imdb_id):
        """return title name"""

        # check if valid imdb_id
        if valid_id(imdb_id):
            return imdb.get_title(imdb_id)["base"]['title']

        else:
            return False

    def title_year(imdb_id):
        """return title year"""

        # check if valid imdb_id
        if valid_id(imdb_id):
            try:
                return imdb.get_title(imdb_id)["base"]['year']
            except:
                return "Sorry, no year found!"
        else:
            return False

    def title_poster(imdb_id, check = 0):
        """return title poster"""

        # check if valid imdb_id
        if valid_id(imdb_id):

            # prevent searching in the same database
            if check == 0:
                # check if there is a poster
                try:
                    return imdb.get_title(imdb_id)["base"]["image"]['url']

                # if there is no poster try to find image
                except:

                    try:
                        return (imdb.get_title_images(imdb_id)['images'][0]['url'])

                    # if there is no image return image not found image
                    except:
                        return "http://www.gentsbierfestival.be/sites/default/files/default_images/notfound.jpg"

            # do not search in imdb_get_title
            if check == 1:
                try:
                    return (imdb.get_title_images(imdb_id)['images'][0]['url'])

                # if there is no image return image not found image
                except:
                    return "http://www.gentsbierfestival.be/sites/default/files/default_images/notfound.jpg"
        else:
            return False

    def title_summary(imdb_id):
        """return title summary"""

        # check if valid imdb_id
        if valid_id(imdb_id):

            try:
                plot_summary = imdb.get_title_plot(imdb_id)

                # if there are no summaries return short plot
                if plot_summary["totalSummaries"] == 0:

                    # if there are no summaries put outline in dic
                    return plot_summary["outline"]['text']

                # check if there are summuries
                else:
                    # put summary in dic
                    return plot_summary["summaries"][0]['text']
            except:
                return "Sorry, no plot found!"

        else:
            return False

    def title_genres(imdb_id):
        """return title genre(s)"""

        # check if valid imdb_id
        if valid_id(imdb_id):

            try:
                # get genre list
                genres = imdb.get_title_genres(imdb_id)["genres"]

                s = ''

                # turn list in string
                for genre in genres:

                    if not s:
                        s = s + genre

                    else:
                        s = s + ", " + genre

                return s
            except:
                return "Sorry, no genre(s) found!"

        else:
            return False

    def title_rating(imdb_id):
        """return title rating"""

        # check if valid imdb_id
        if valid_id(imdb_id):

            try:
                return imdb.get_title_ratings(imdb_id)["rating"]
            except:
                return "Sorry, no rating found!"

        else:
            return False

    def add_item(film_id):
        """adds item to items"""

        db.execute("INSERT INTO films (film_id, title, summary, year, image) VALUES (:film_id, :title, :summary, :year, :image)", film_id = film_id, title = Search.title_name(film_id), summary = Search.title_summary(film_id),
        year = Search.title_year(film_id), image = Search.title_poster(film_id))

    def community(community):
        """searches a community and returns list of similiarcommunitties"""

        communities_found = []

        # request name and description from database
        rows = db.execute("SELECT name,description FROM community_page")


        # check if name is similiar to search
        for row in rows:

            community_found = {}

            # correct search for capital letters
            name_lower = row["name"].lower()
            community_lower = community.lower()

            # check for special signs
            for old, new in [("@", "a"), ("|", "i"), ("0", "o")]:
                name_lower = name_lower.replace(old, new)
                community_lower = community_lower.replace(old, new)

            # if similair community found add to list
            if name_lower.find(community_lower) != -1:

                # add name to list
                community_found["name"] = row["name"]

                # add description to list
                community_found["description"] = row["description"]

                # add members amount to list
                community_found["members amount"] = len(db.execute("SELECT username FROM community_users WHERE communityname=:communityname", communityname=row["name"]))

                communities_found.append(community_found)

        return communities_found
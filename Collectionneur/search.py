from cs50 import SQL
from helpers import valid_id, valid_id_actor

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

                # extract dic from one list
                movie_info = info_database[0]

                # change film_id to imdb_id and summary to short plot
                movie_info['imdb_id'] = movie_info.pop("film_id")
                movie_info['short plot'] = movie_info.pop("summary")

                # put the movie_info in a list
                all_movie_info.append(movie_info)

            # do if imdb_id exist and movie not in database
            elif valid_id(title_results[i]["imdb_id"]):

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

                # try to find movie poster
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

            # try to find movie poster
            try:
                # put a movie image in the dic
                full_movie_info["image"] = title_info_id["base"]["image"]['url']
            except:
                # try to find related image else put image not found image in dic
                full_movie_info["image"] = Search.title_poster(imdb_id, check = 1)

            # try to find a summary else put outline in dic
            full_movie_info["plot"] = Search.title_summary(imdb_id)

            # try to get genre list
            full_movie_info["genre"] = Search.title_genres(imdb_id)

            # try to get movie rating
            full_movie_info["rating"] = Search.title_rating(imdb_id)

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

                # check if there are summaries
                else:
                    # put summary in dic
                    return plot_summary["summaries"][0]['text']

            # notify user that no plot is found
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

    def community(community):
        """searches a community and returns list of similar communities"""

        communities_found = []

        # request name and description from database
        rows = db.execute("SELECT name,description FROM community_page")

        # check if name is similar to search
        for row in rows:

            community_found = {}

            # correct search for capital letters
            name_lower = row["name"].lower()
            community_lower = community.lower()

            # check for special signs
            for old, new in [("@", "a"), ("|", "i"), ("0", "o")]:
                name_lower = name_lower.replace(old, new)
                community_lower = community_lower.replace(old, new)

            # if similar community found add to list
            if name_lower.find(community_lower) != -1:

                # add name to list
                community_found["name"] = row["name"]

                # add description to list
                community_found["description"] = row["description"]

                # add members amount to list
                community_found["members amount"] = len(db.execute("SELECT username FROM community_users WHERE communityname=:communityname", communityname=row["name"]))

                communities_found.append(community_found)

        return communities_found

    def search_actor(to_search):
        """returns short actor information"""

        actors = imdb.search_for_name(to_search)

        actors_information = []

        for actor in actors:

            actor_information = Search.actor_information(actor["imdb_id"])

            actors_information.append(actor_information)

        return actors_information

    def actor_information(actor_id):
        """return actor information"""

        if valid_id_actor(actor_id):

            actor_information = {}

            # get actor id
            actor_information["actor_id"] = actor_id

            # get actor information
            actor_info = imdb.get_name(actor_id)

            # get actor name
            try:
                actor_information["actor_name"]  = actor_info["actor_name"]

            except:
                try:
                    actor_information["actor_name"]  = actor_info["base"]["name"]

                # this is just to see if the key is different e.g. returns name but in a different path at the end it will return an empty string because not knowing a name but giving it as result is just weird.
                except:
                    actor_information["actor_name"] = "Something went wrong when trying to fetch this actors name!"

            # look for image of actor
            try:
                actor_information["image"] = actor_info["base"]["image"]["url"]

            except:
                actor_information["image"] = "http://www.gentsbierfestival.be/sites/default/files/default_images/notfound.jpg"

            # look for birthdate
            try:
                actor_information["birthdate"] = actor_info["base"]["birthDate"]

            except:
                actor_information["birthdate"] = "could not find birthdate"

            # look for actor trademarks
            try:
                actor_information["trademarks"] = actor_info["base"]["trademarks"][0]

            except:
                actor_information["trademarks"] = "could not find trademarks"

            # look for actor jobs
            try:
                actor_information["jobs"] = ', '.join(actor_info["jobs"])

            except:
                actor_information["jobs"] = "could not find jobs"

            # look for mini bios
            try:
                actor_information["minibios"] = actor_info["base"]["miniBios"][0]["text"]

            except:
                actor_information["minibios"] = "could not find mini bios"

            return actor_information

    def actor_movies(actor_id):
        """returns dic of actors most recent movies"""

        films = (imdb.get_name_filmography(actor_id)["filmography"])
        teller = 0
        recent_movies = []

        # loop trough films actor played role in
        for film in films:

            futured_films = {}

            # check if film is released
            if film["status"] == 'released':

                # try to get all required information
                try:
                    # filter film id from /title/film_id/
                    futured_films["film_id"] = film["id"][7:16]

                    futured_films["image"] = film["image"]["url"]

                    futured_films["title"] = film["title"]

                    recent_movies.append(futured_films)

                    teller += 1

                # if not all info found skip movie
                except:
                    futured_films = {}

            # only get first 5 movies
            if teller == 5:
                return recent_movies

        # return list of movies actor played if it is less than 5
        return recent_movies

    def movie_actors(imdb_id):
        """returns list of movie actors"""

        # get cast members
        actors = imdb.get_title_credits(imdb_id)["credits"]["cast"]

        teller = 0
        movie_actors = []

        # loop trough each cast member
        for actor in actors:

            movie_actor= {}

            # check if cast member is really an actor or actress
            if actor["category"] == 'actor' or actor["category"] == "actress":

                # try to get all required information
                try:
                    # filter actor id from /name/actor_id/
                    movie_actor["actor_id"] = actor["id"][6:15]

                    movie_actor["image"] = actor["image"]["url"]

                    movie_actor["name"] = actor["name"]

                    movie_actors.append(movie_actor)

                    teller += 1

                # if not all info found skip actor/actress
                except:
                    movie_actor = {}

            # only get first 5 actors
            if teller == 5:
                return movie_actors

        # return list of actors played in movie if it is less than 5
        return movie_actors

    def similar_films(imdb_id):
        """returns list of similar_films"""

        # get all similar films
        similarities = imdb.get_title_similarities(imdb_id)["similarities"]

        teller = 0
        similar_titles = []

        # loop trough each film
        for title in similarities:

            similar_title = {}

            # check if similar title is not the same movie
            if not title["id"][7:16] == imdb_id:

                # try to get all required information
                try:
                    # filter film id from /title/film_id/
                    similar_title["imdb_id"] = title["id"][7:16]

                    similar_title["image"] = title["image"]["url"]

                    similar_title["title"] = title["title"]

                    similar_titles.append(similar_title)

                    teller += 1

                # if not all info found skip movie
                except:
                    similar_title = {}

                # only get first 5 films
                if teller == 5:
                    return similar_titles

        #return list of similar films if it is less than 5
        return similar_titles

from imdbpie import Imdb
imdb = Imdb()

class Home():
    def get_popular_movies():
        """returns dic of ranks"""

        poptitles = imdb.get_popular_titles()["ranks"]
        ranks = {}

        for i in range(10):
            ranks[i + 1] = poptitles[i]["title"]

        return ranks
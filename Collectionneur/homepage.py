from imdbpie import Imdb
imdb = Imdb()

class Home():
    def get_popular_movies():
        """returns dic of ranks"""

        poptitles = imdb.get_popular_movies()["ranks"]
        ranks = []
        for item in poptitles:
            rank = {}
            rank["rank"] = item["currentRank"]
            rank["title"] = item["title"]
            rank["id"] = item["id"][7:-1]
            ranks.append(rank)


        return ranks[:10]
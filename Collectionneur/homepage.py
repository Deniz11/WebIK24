from imdbpie import Imdb
imdb = Imdb()

class Home():
    def get_popular_movies():
        lijst = []
        popular = imdb.get_popular_movies()
        for i in range(len(popular))
            lijst += i
        return lijst

    def
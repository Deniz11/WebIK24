from imdbpie import Imdb
imdb = Imdb()

class Home():
    def get_popular_movies():
        popular = imdb.get_popular_titles()
        return render_template("index.html", popular=popular)
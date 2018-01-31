from communities import Communities as com
from search import Search
from imdbpie import Imdb
imdb = Imdb()

class Home():

    # Return popular movies and information.
    def get_popular_movies():
        """returns dic of ranks"""

        # Use API for ranks.
        poptitles = imdb.get_popular_movies()["ranks"]
        ranks = []

        # Convert poptitles to workable list of dicts.
        # Also add more information.
        for item in poptitles[:6]:
            rank = {}
            rank["rank"] = item["currentRank"]
            rank["title"] = item["title"]
            rank["id"] = item["id"][7:-1]
            rank["image"] = item["image"]["url"]
            rank["summary"] = Search.title_summary(rank["id"])
            ranks.append(rank)

        return ranks

    # Rank the communities for the homepage.
    def rank_communities():
        # Get all communities
        coms = com.show()
        coms_tuples = []
        ranks=[]

        # Transform in workable format (tuples).
        for item in coms:
            # Give communities score based on items and members.
            coms_tuples.append((item["name"], len(com.showmembers(item["name"]))+len(com.showlist(com.get_list_id(item["name"]))), item["description"]))

        # Save ranks in list
        for i in range(len(coms_tuples)):
            rank = {}
            top = max(coms_tuples,key=lambda item:item[1])
            coms_tuples = list(filter(lambda x: x[0] != top[0], coms_tuples))
            rank["rank"] = i+1
            rank["name"]=top[0]
            rank["description"]=top[2]
            ranks.append(rank)

        return ranks[:5]


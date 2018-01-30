from communities import Communities as com
from imdbpie import Imdb
imdb = Imdb()

class Home():
    def get_popular_movies():
        """returns dic of ranks"""

        poptitles = imdb.get_popular_movies()["ranks"]
        ranks = []
        for item in poptitles[:6]:
            rank = {}
            rank["rank"] = item["currentRank"]
            rank["title"] = item["title"]
            rank["id"] = item["id"][7:-1]
            rank["image"] = item["image"]["url"]
            ranks.append(rank)


        return ranks
    def rank_communities():
        coms = com.show()
        coms_tuples = []
        ranks=[]
        for item in coms:
            # get list length
            coms_tuples.append((item["name"], len(com.showmembers(item["name"]))+len(com.showlist(com.get_list_id(item["name"]))), item["description"]))
        for i in range(len(coms_tuples)):
            rank = {}
            top = max(coms_tuples,key=lambda item:item[1])
            coms_tuples = list(filter(lambda x: x[0] != top[0], coms_tuples))
            rank["rank"] = i+1
            rank["name"]=top[0]
            rank["description"]=top[2]
            ranks.append(rank)
        return ranks[:5]


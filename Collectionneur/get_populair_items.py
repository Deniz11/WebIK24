from search import Search
from helpers import *
from communities import Communities as com

#print(len(imdb.get_popular_titles()["ranks"]))
poptitles = imdb.get_popular_titles()["ranks"]
for i in range(len(poptitles)):
    print(poptitles[i]["title"])


#print(valid_id("tt0303461"))

#print(Search.community("China"))

#print(Search.search_titles("star wars"))

#print(Search.title_info("tt2527336"))

#print(Search.title_name("tt2527336"))

#print(Search.title_year("tt2527336"))

#print(Search.title_poster("tt2527336"))

#print(Search.title_summary("tt2527336"))

#print(Search.title_genres("tt2527336"))

#print(Search.title_rating("tt2527336"))

# Search.add_item("tt0303461")

#print(Search.search_titles("mo"))

# test.pyprint(imdb.get_title("tt2527336"))

#print(com.members("ChinaHaters"))tt6218010

#print(imdb.get_title("tt2527336"))

#print(imdb.get_title('tt0111161')["plot"])

#print((imdb.get_title("tt4728328")))
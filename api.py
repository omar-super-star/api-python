import requests_with_caching
import json
def get_movies_from_tastedive(s):
    base="https://tastedive.com/api/similar"
    parm={"q":s,"type":"movies","limit":5}
    res=requests_with_caching.get(base,params=parm)
    return json.loads(res.text)
def extract_movie_titles(s):
    movies_title=[]
    for i in s["Similar"]["Results"]:
        movies_title.append(i["Name"])
    return movies_title
def get_related_titles(s):
    last=[]
    if s != [] and len(s)!=1:
        last.extend(extract_movie_titles(get_movies_from_tastedive(s[0])))
        last.extend(extract_movie_titles(get_movies_from_tastedive(s[1])))
        return list(set(last))
    return []
def get_movie_data(s):
    base="http://www.omdbapi.com/"
    parm={"t":s,"r":"json"}
    res=requests_with_caching.get(base,params=parm)
    print(json.loads(res.text))
    return json.loads(res.text)
def get_movie_rating(p):
    if len(p["Ratings"])>=2: 
        if p["Ratings"][1]["Source"] == 'Rotten Tomatoes':
            return int(p["Ratings"][1]["Value"][:2])
        return 0
    else:
        for i in p["Ratings"]:
            if i.get("Source",0) != 0:
                if i.get("Source") == 'Rotten Tomatoes':
                    return int(i.get("Value")[:2])
                return 0
        return 0
def get_sorted_recommendations(s):
    first=get_related_titles(s)
    print(first)
    if first != []:
        finish=sorted(first,key=lambda x:(get_movie_rating(get_movie_data(x)),x[0]),reverse=True)
        return finish
                

import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0"
}

urls = [
"https://en.wikipedia.org/wiki/Babygirl",
"https://en.wikipedia.org/wiki/A_Big_Case",
"https://en.wikipedia.org/wiki/Titanic_(1997_film)",
"https://en.wikipedia.org/wiki/Inception",
"https://en.wikipedia.org/wiki/Interstellar_(film)",
"https://en.wikipedia.org/wiki/Avatar_(2009_film)",
"https://en.wikipedia.org/wiki/The_Dark_Knight",
"https://en.wikipedia.org/wiki/Joker_(2019_film)",
"https://en.wikipedia.org/wiki/Gladiator_(2000_film)",
"https://en.wikipedia.org/wiki/The_Godfather",
"https://en.wikipedia.org/wiki/Pulp_Fiction",
"https://en.wikipedia.org/wiki/Fight_Club",
"https://en.wikipedia.org/wiki/Forrest_Gump",
"https://en.wikipedia.org/wiki/The_Matrix",
"https://en.wikipedia.org/wiki/The_Lord_of_the_Rings:_The_Fellowship_of_the_Ring",
"https://en.wikipedia.org/wiki/The_Lord_of_the_Rings:_The_Two_Towers",
"https://en.wikipedia.org/wiki/The_Lord_of_the_Rings:_The_Return_of_the_King",
"https://en.wikipedia.org/wiki/Avengers:_Endgame",
"https://en.wikipedia.org/wiki/Iron_Man_(2008_film)",
"https://en.wikipedia.org/wiki/Spider-Man_(2002_film)",
"https://en.wikipedia.org/wiki/Whiplash_(2014_film)",
"https://en.wikipedia.org/wiki/Dune_(2021_film)",
"https://en.wikipedia.org/wiki/No_Time_to_Die",
"https://en.wikipedia.org/wiki/Skyfall",
"https://en.wikipedia.org/wiki/Doctor_Strange_(2016_film)",
"https://en.wikipedia.org/wiki/Black_Panther_(film)",
"https://en.wikipedia.org/wiki/Deadpool_(film)",
"https://en.wikipedia.org/wiki/Logan_(film)",
"https://en.wikipedia.org/wiki/Mad_Max:_Fury_Road"
]

data = []

for url in urls:
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("h1")
        if not title_tag:
            continue

        title = title_tag.text.strip()

        infobox = soup.find("table", {"class": "infobox"})
        if not infobox:
            continue

        rows = infobox.find_all("tr")

        director = None
        actors = []

        for row in rows:
            header = row.find("th")
            value = row.find("td")

            if header and value:
                if "Directed by" in header.text:
                    director = value.text.strip()

                if "Starring" in header.text:
                    actors = [a.strip() for a in value.text.split("\n") if a.strip()]

        if director and actors:
            for actor in actors:
                data.append({
                    "film": title,
                    "director": director,
                    "actor": actor
                })

    except:
        continue

print("Nombre de lignes :", len(data))

df = pd.DataFrame(data)

df.to_csv("../data/crawled_movies.csv", index=False)

print(df.head())
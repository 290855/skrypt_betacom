from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://rpa.hybrydoweit.pl/'
respond = requests.get(url)
soup = BeautifulSoup(respond.content, 'html.parser')

divTag = soup.find_all("div", {"class": "rpa-container rpajs-articles"})
tdTags = divTag[0].find_all("article", {"class": "rpa-article-card"})

list = []
for tag in tdTags:
    title = tag.find("h3", {"class": "rpa-article-card__title"})
    metadata = tag.find("li", {"class": "rpa-article-card__metadata-item"})
    href = tag.find("a", {"class": "rpa-article-card__link"})
    list.append([title.text, metadata.text, href['href']])

data = pd.DataFrame(list, columns=['tytuł', 'branża/dział', 'link'])
data.to_excel("out.xlsx", sheet_name="sheet_1")
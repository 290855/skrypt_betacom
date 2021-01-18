import pandas as pd
import requests
from bs4 import BeautifulSoup

class Robot:
    def __init__(self):
        _url = 'https://rpa.hybrydoweit.pl/'
        _respond = requests.get(_url)
        _soup = BeautifulSoup(_respond.content, 'html.parser')
        self.divTag = _soup.find_all("div", {"class": "rpa-container rpajs-articles"})
        self.fileName = "output.xlsx"
        self.sheetName = "sheet_1"

    def articleFrameCountCheck(self) -> bool:
        return (len(self.divTag) == 1)

    def collectData(self):
        tdTags = self.divTag[0].find_all("article", {"class": "rpa-article-card"})

        list = []

        for tag in tdTags:
            title = tag.find("h3", {"class": "rpa-article-card__title"})
            metadata = tag.find("li", {"class": "rpa-article-card__metadata-item"})
            href = tag.find("a", {"class": "rpa-article-card__link"})

            list.append([title.text, metadata.text, href['href']])

        data = pd.DataFrame(list, columns=['tytuł', 'branża/dział', 'link'])
        return data

    def makeExcelFile(self):
        if self.articleFrameCountCheck():
            self.collectData().to_excel(self.fileName, sheet_name=self.sheetName)

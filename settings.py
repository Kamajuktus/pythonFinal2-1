from scrap import news_scraper
from models import addNews, getTheNews
coinScraper = news_scraper()


def insertResults(cryptoname):
    result = coinScraper.find_coin_news(cryptoname)
    for news in result:
        title = cryptoname
        link = news.find('a', href=True)["href"]
        paragraphs = coinScraper.ScrapTheLink(link)
        addNews(title, link, paragraphs)

def GetResults():
    newsets =  getTheNews()
    return newsets



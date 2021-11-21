from bs4 import BeautifulSoup
import requests


class news_scraper():

    urls = []

    def find_coin_news(self, query):
    
        url = 'https://www.coingecko.com/en/coins/' + query + '/news'
        page = requests.get(url)
        news_parser = BeautifulSoup(page.content, 'html.parser')
        page_currency_news_title2 = news_parser.find_all("div", class_ = "my-4")

        return page_currency_news_title2

    def ScrapTheLink(self, link):
        url = link
        page = requests.get(url)
        news_parser = BeautifulSoup(page.content, 'html.parser')
        results = []
        linkPageScraper = news_parser.find_all("p")
        for news in linkPageScraper:
            results.append(news.text.strip() + '\n')
        return results



        
import requests
from scrapy.http import TextResponse

url = "http://quotes.toscrape.com"


class Quotes:
    def __init__(self, url):
        self.url = url
        self.page = requests.get(self.url)
        self.response = TextResponse(body=self.page.text, url=self.url, encoding="utf-8")

    def get_quote_info(self):
        does_next_page_exist = True
        authors = []
        quotes = []
        tags = []
        while does_next_page_exist:
            authors += self.__get_authors()
            quotes += self.__get_quotes()
            tags += self.__get_tags()
            does_next_page_exist = self.__is_next_page_available()
        return authors, quotes, tags

    def __get_authors(self):
        authors = (self.response.css("small.author::text").extract())
        return authors

    def __get_quotes(self):
        quotes = self.response.css("span.text::text").extract()
        return quotes

    def __get_tags(self):
        tags = [i.css("a.tag::text").extract() for i in self.response.css("div.tags")]
        return tags

    def __is_next_page_available(self):
        next_page_path = self.response.css("li.next a::attr(href)").extract_first()
        if next_page_path is not None:
            next_url = self.url + next_page_path
            self.page = requests.get(next_url)
            self.response = TextResponse(body=self.page.text, url=next_url, encoding="utf-8")
            return True
        else:
            return False


quotes_page = Quotes(url)
print(quotes_page.get_quote_info())


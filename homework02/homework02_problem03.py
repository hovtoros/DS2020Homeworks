import requests
from scrapy.http import TextResponse

url = "http://books.toscrape.com"


class Books:
    def __init__(self, url):
        self.url = url
        self.page = requests.get(self.url)
        self.response = TextResponse(body=self.page.text, url=self.url, encoding="utf-8")

    def get_books_info(self):
        does_next_page_exist = True
        titles = []
        prices = []
        books_url = []
        books_picture_url = []
        books_stock = []
        while does_next_page_exist:
            titles += self.__get_titles()
            prices += self.__get_prices()
            books_url += self.__get_book_url()
            books_picture_url += self.__get_book_picture_url()
            books_stock += self.__get_book_stock()
            does_next_page_exist = self.__is_next_page_available()
        return titles, prices, books_url, books_picture_url, books_stock

    def __get_titles(self):
        return self.response.css("p.star-rating ~ h3 > a::attr(title)").extract()

    def __get_prices(self):
        return self.response.css("div.product_price > p.price_color::text").extract()

    def __get_book_url(self):
        return self.response.css("p.star-rating ~ h3 > a::attr(href)").extract()

    def __get_book_picture_url(self):
        return self.response.css("div.image_container img::attr(src)").extract()

    def __get_book_stock(self):
        return self.response.css("p.instock::text").extract()

    def __is_next_page_available(self):
        next_page_path = self.response.css("li.next a::attr(href)").extract_first()
        if next_page_path is not None:
            next_url = self.url + "/catalogue" + next_page_path
            self.page = requests.get(next_url)
            self.response = TextResponse(body=self.page.text, url=next_url, encoding="utf-8")
            return True
        else:
            return False


books_page = Books(url)
print(books_page.get_books_info())


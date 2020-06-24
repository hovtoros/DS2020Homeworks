# -*- coding: utf-8 -*-
import scrapy


class ImdbBotSpider(scrapy.Spider):
    name = 'imdbBot'
    allowed_domains = ['https://www.imdb.com/chart/moviemeter/']
    start_urls = ['https://www.imdb.com/chart/moviemeter//']

    def parse(self, response):
        titles = response.css('td.titleColumn > a::text').extract()
        years = response.css('td.titleColumn > span.secondaryInfo::text').extract()
        ranking = response.css('td.titleColumn > div.velocity::text').extract()
        rating = response.css('td.ratingColumn > strong::text').extract()
        hyperlink = response.css('td.titleColumn > a::attr(href)').extract()

        for item in zip(titles, years, ranking, rating, hyperlink):
            scraped_info = {
                'title': item[0],
                'year': item[1],
                'ranking': item[2],
                'rating': item[3],
                'hyperlink': item[4]
            }

            yield scraped_info

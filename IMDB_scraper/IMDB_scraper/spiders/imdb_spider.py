# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt2442560/']
    
    def parse(self, response):
        link = self.start_urls[0] + 'fullcredits'
        yield scrapy.Request(link, callback = self.parse_full_credits)
    
    def parse_full_credits(self, response):
        actors = response.xpath('//td[not(@class)]/a/@href').extract()
        for actor in actors:
            complete_url = 'https://www.imdb.com/' + actor
            yield scrapy.Request(complete_url, callback = self.parse_actor_page)
        
    def parse_actor_page(self, response):
        movies = response.css("div.filmo-row").css("div[id^='actor']").css("a:not(.in_production)::text").extract()
        actor_name = response.css("div.article.name-overview.with-hero").css("span::text").extract_first()
        for x in movies:
            yield {
                'actor' : actor_name,
                'movie_or_TV_name' : x
            }


    
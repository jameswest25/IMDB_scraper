# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt2442560/']
    
    def parse(self, response):
        '''
        docstring:
        Assumptions: this method will be called on an IMDB title page, 
        in this case the Peaky Blinders title page.
        Effect: this method sends the spider from an IMDB title page,
        to the page for Cast and Crew. It yields a scrapy request that
        calls the next method, parse_full_credits, on the new page. 
        '''
        link = self.start_urls[0] + 'fullcredits' #this line adds the 
        #phrase fullcredits to the start URL, which coincidentally
        #is the url for the cast and crew of the production
        yield scrapy.Request(link, callback = self.parse_full_credits)
        #this line yields a scrapy request, sending the spider to the
        #link specified by the variable link. It then calls the 
        #method parse_full_credits on this page.
    
    def parse_full_credits(self, response):
        '''
        docstring
        Assumptions: this method will be called on an IMDB cast and
        crew page, in this case the Peaky Blinders cast and crew page
        Effect: this method first scans the page for the list of 
        actors, then compiles the proper url phrases for each actor.
        Then, with this list of url phrases, we add https://www.imdb.com/
        to the front and yield a scrapy request for the resulting
        url string, calling the method, parse_actor_page, on the
        new page. 
        '''
        actors = response.xpath('//td[not(@class)]/a/@href').extract()
        #This line takes advantage of unique html tags for the actor
        #list to scrape the links for the actors. However, this list
        #of strings are not complete urls, so a little editing is needed. 
        for actor in actors:
        #This is a for loop, which is used to access one item in a list at a time
            complete_url = 'https://www.imdb.com/' + actor
            #This line adds the above phrase to each item in the list actor,
            #making each item into a usable url. 
            yield scrapy.Request(complete_url, callback = self.parse_actor_page)
            #This line yields a scrapy request, sending the spider to the link
            #specified by the variable complete_url, which is the actor page.
            #Then on this page, it calls the method parse_actor_page.
        
    def parse_actor_page(self, response):
        '''
        docstring
        Assumptions: this method will be called on an IMDB actor page, 
        in this case the Peaky Blinders' actors' pages.
        Effects: this method first leads the scraper to look at elements 
        with the class filmo-row and then I specified to only include 
        elements with the Id tag starting with actor. I then scraped all 
        the text without the in_production class and extracted to get all 
        the movie titles. To get the actor name, I just looked at the actor
        overview and then scraped the text and extracted the first element 
        to get the character name. To finish, I yield a dictionary with the 
        actor name and movies they are in.
        '''
        movies = response.css("div.filmo-row").css("div[id^='actor']").css("a:not(.in_production)::text").extract()
        #this line first leads the spider to look at elements 
        #in the filmography sections and then I specified to only include 
        #elements with the Id tag starting with actor. I then scraped all 
        #the text without the in_production class and extracted to get all 
        #the movie titles.
        actor_name = response.css("div.article.name-overview.with-hero").css("span::text").extract_first()
        #In this line, the spider looks at the actor page overview and then 
        #scrapes the text and extracts the first element to get the character name.
        for x in movies:
        #This is a for loop, which is used to access one item in a list at a time
            yield {
                'actor' : actor_name,
                'movie_or_TV_name' : x
            }
        #These lines yield a dictionary with the actor name and a movie they were in


    
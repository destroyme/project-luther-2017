# -*- coding: utf-8 -*-
import scrapy
import pickle

# with open("BOMojo_movie_links.pkl", 'rb') as picklefile: 
    # _movieurls = pickle.load(picklefile)

class MoviesSpider(scrapy.Spider):
    name = "movies"
    allowed_domains = ["boxofficemojo.com"]
    custom_settings = {
                 "DOWNLOAD_DELAY": 1,
                 "CONCURRENT_REQUESTS_PER_DOMAIN":2,
                 "BOT_NAME":'inv',
                 "ROBOTSTXT_OBEY":False}

    def start_requests(self):
        # with open("BOMojo_movie_links.pkl", 'rb') as picklefile: 
        #     _movieurls = pickle.load(picklefile)
        _movieurls = ['http://www.boxofficemojo.com/movies/?id=murderball.htm']#, 
                    #   'http://www.boxofficemojo.com/movies/?id=betterthanchocolate.htm']
        for link in _movieurls:
            url = link + '&adjust_yr=2017&p=.htm'
            yield scrapy.Request(url=url, callback = self.getMovies)

    
    def getMovies(self, response):
        try:
            movie_title = response.xpath('//font/b/text()')[0].extract()
        except:
            movie_title = response.url
        
        try:
            directors = response.xpath("//a[contains(., 'Director')]/../../following-sibling::td[1]/descendant::*/text()").extract()
        except:
            directors = None
        
        try:
            writers = response.xpath("//a[contains(., 'Writers')]/../../following-sibling::td[1]/descendant::*/text()").extract()
        except:
            writers = None
        
        try:
            actors = response.xpath("//a[contains(., 'Actors')]/../../following-sibling::td[1]/descendant::*/text()").extract()
        except:
            actors = None

        try:
            producers = response.xpath("//a[contains(., 'Producers')]/../../following-sibling::td[1]/descendant::*/text()").extract()
        except:
            producers = None
        
        try:
            composers = response.xpath("//a[contains(., 'Composer')]/../../following-sibling::td[1]/descendant::*/text()").extract()
        except:
            composers = None
        
        yield { movie_title : { 'directors' : directors,
                                'writers' : writers,
                                'actors' : actors,
                                'producers' : producers,
                                'composers' : composers
                              }}


                # {"a": {x=1}}
                # {"b": {x=1}}
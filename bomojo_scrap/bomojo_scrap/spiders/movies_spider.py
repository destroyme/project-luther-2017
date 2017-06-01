# -*- coding: utf-8 -*-
import scrapy
import pickle

# with open("BOMojo_movie_links.pkl", 'rb') as picklefile: 
    # _movieurls = pickle.load(picklefile)

class MoviesSpider(scrapy.Spider):
    name = "movies"
    allowed_domains = ["boxofficemojo.com"]
    custom_settings = {
                #  "DOWNLOAD_DELAY": 1,
                #  "CONCURRENT_REQUESTS_PER_DOMAIN":2,
                 "BOT_NAME":'inv',
                 "ROBOTSTXT_OBEY":False}

    def start_requests(self):
        with open("BOMojo_movie_links.pkl", 'rb') as picklefile: 
            _movieurls = pickle.load(picklefile)
        # _movieurls = ['http://www.boxofficemojo.com/movies/?id=murderball.htm', 
        #               'http://www.boxofficemojo.com/movies/?id=betterthanchocolate.htm']
        for link in _movieurls:
            url = link + '&adjust_yr=2017&p=.htm'
            yield scrapy.Request(url=url, callback = self.getMovies)
    
    def findCrew(self, crew):
        crew_actual = []
        for cm in crew:
            extract = cm.extract()
            if extract != ' ':
                crew_actual.append(extract)
        return crew_actual

    
    def getMovies(self, response):
        try:
            # movie_title = response.xpath('//font/b/text()')[0].extract()
            movie_title = response.xpath("//font[@face='Verdana']/b/descendant-or-self::*/text()").extract()
            if isinstance(movie_title, list):
                movie_title = ' '.join(movie_title)
            elif isinstance(movie_title, str):
                pass
        except:
            movie_title = response.url

        try:
            domestic_gross_adj = response.xpath("//font[contains(text(),'Domestic')]/b/text()").extract_first()
        except:
            domestic_gross_adj = None

        try:
            distributor = response.xpath("//td[contains(text(),'Distributor')]/b/descendant-or-self::*/text()").extract_first()
        except:
            distributor = None
        
        try:
            # foreign_unadj = response.xpath("//td[@align='right' and @width='35%']/text()")[1].extract()
            foreign_unadj = response.xpath("//a[contains(text(),'Foreign:')]/../following-sibling::td[1]/text()").extract_first()
        except:
            foreign_unadj = None

        try:
            # worldwide_gross_unadj = response.xpath("//td[@width='35%']/b/text()")[1].extract()
            worldwide_gross_unadj = response.xpath("//b[contains(text(),'Worldwide:')]/../following-sibling::td[1]/descendant::*/text()").extract_first()
        except:
            worldwide_gross_unadj = None

        try:
            # release_date = response.xpath('//nobr/a/text()')[0].extract()
            release_date = response.xpath("//td[contains(text(),'Release Date')]/b/descendant-or-self::*/text()").extract_first()
        except:
            release_date = None

        try:
            # genre = response.xpath('//td/b/text()')[0].extract()
            genre = response.xpath("//td[contains(text(),'Genre')]/b/descendant-or-self::*/text()").extract_first()
        except:
            genre = None
        
        try:
            # runtime = response.xpath('//td/b/text()')[1].extract()
            runtime = response.xpath("//td[contains(text(),'Runtime')]/b/descendant-or-self::*/text()").extract_first()
        except:
            runtime = None
        
        try:
            # mpaa_rating = response.xpath('//td/b/text()')[2].extract()
            mpaa_rating = response.xpath("//td[contains(text(),'MPAA Rating')]/b/descendant-or-self::*/text()").extract_first()
        except:
            mpaa_rating = None

        try:
            # production_budget_adj = response.xpath('//td/b/text()')[3].extract()
            production_budget_adj = response.xpath("//td[contains(text(),'Production Budget')]/b/descendant-or-self::*/text()").extract_first()
        except:
            production_budget_adj = None 
        
        try:
            # opening_weekend_adj = response.xpath("//tr[count(td)=2]/td/text()")[8].extract()
            opening_weekend_adj = response.xpath("//a[contains(@href,'/weekend/chart/?yr=')]//../following-sibling::td[1]/text()").extract_first()
        except:
            opening_weekend_adj = None
        
        try:
            # number_of_theaters = response.xpath("//tr[count(td)=2]/td/text()")[12].extract()
            number_of_theaters = response.xpath("//td[contains(text(),'Widest')][1]//.//following-sibling::td[1]/text()").extract_first()
        except:
            number_of_theaters = None
        
        try:
            # close_date = response.xpath("//tr[count(td)=2]/td/text()")[14].extract()
            close_date = response.xpath("//td[contains(text(),'Close')][1]//.//following-sibling::td[1]/text()").extract_first()
        except:
            close_date = None

        try:
            # days_in_theater = response.xpath("//tr[count(td)=2]/td/text()")[16].extract()
            days_in_theater = response.xpath("//td[contains(text(),'In Release')][1]//.//following-sibling::td[1]/text()").extract_first()
        except:
            days_in_theater = None


        # --------------
        #  CREW
        # --------------

        try:
            # directors = response.xpath("//a[contains(., 'Director')]/../../following-sibling::td[1]/descendant::*/text()").extract()
            directors_raw = response.xpath("//a[contains(., 'Director')]/../../following-sibling::td[1]/font//text()[not(contains(.,'(') or contains(.,'*') or self::br)]")
            directors = self.findCrew(directors_raw)
            # self.logger.info('### Directors : %s', directors)
        except:
            directors = None
        
        try:
            # writers = response.xpath("//a[contains(., 'Writer')]/../../following-sibling::td[1]/descendant::*/text()").extract()
            writers_raw = response.xpath("//a[contains(., 'Writer')]/../../following-sibling::td[1]/font//text()[not(contains(.,'(') or contains(.,'*') or self::br)]")
            writers = self.findCrew(writers_raw)
            # self.logger.info('### Writers : %s', writers)
        except:
            writers = None
        
        try:
            # actors = response.xpath("//a[contains(., 'Actor')]/../../following-sibling::td[1]/descendant::*/text()").extract()
            actors_raw = response.xpath("//a[contains(., 'Actor')]/../../following-sibling::td[1]/font//text()[not(contains(.,'(') or contains(.,'*') or self::br)]")
            actors = self.findCrew(actors_raw)
            # self.logger.info('### Actors : %s', actors)
        except:
            actors = None

        try:
            # producers = response.xpath("//a[contains(., 'Producer')]/../../following-sibling::td[1]/descendant::*/text()").extract()
            producers_raw = response.xpath("//a[contains(., 'Producer')]/../../following-sibling::td[1]/font//text()[not(contains(.,'(') or contains(.,'*') or self::br)]")
            producers = self.findCrew(producers_raw)
        except:
            producers = None

        try:
            cinematographer_raw = response.xpath("//a[contains(., 'Cinematographer')]/../../following-sibling::td[1]/font//text()[not(contains(.,'(') or contains(.,'*') or self::br)]")
            cinematographer = self.findCrew(cinematographer_raw)
        except:
            cinematographer = None
        
        try:
            # composers = response.xpath("//a[contains(., 'Composer')]/../../following-sibling::td[1]/descendant::*/text()").extract()
            composers_raw = response.xpath("//a[contains(., 'Composer')]/../../following-sibling::td[1]/font//text()[not(contains(.,'(') or contains(.,'*') or self::br)]")
            composers = self.findCrew(composers_raw)
        except:
            composers = None
        
        yield { movie_title : { 'domestic_gross_adj' : domestic_gross_adj,
                                'foreign_unadj' : foreign_unadj,
                                'worldwide_gross_unadj' : worldwide_gross_unadj,
                                'release_date' : release_date,
                                'distributor' : distributor,
                                'genre': genre,
                                'runtime': runtime,
                                'mpaa_rating': mpaa_rating,
                                'production_budget_adj': production_budget_adj,
                                'opening_weekend_adj': opening_weekend_adj,
                                'number_of_theaters': number_of_theaters,
                                'close_date': close_date,
                                'days_in_theater': days_in_theater,
                                # crew
                                'directors' : directors,
                                'writers' : writers,
                                'actors' : actors,
                                'producers' : producers,
                                'composers' : composers

                              }}
import scrapy
from scrapy.crawler import CrawlerProcess
import logging


class Booking_data(scrapy.Spider):
    name = 'booking_data'
    list_cities = ["Mont Saint Michel","St Malo","Bayeux","Le Havre","Rouen","Paris","Amiens","Lille","Strasbourg","Chateau du Haut Koenigsbourg","Colmar","Eguisheim","Besancon","Dijon","Annecy","Grenoble","Lyon","Gorges du Verdon","Bormes les Mimosas","Cassis","Marseille","Aix en Provence","Avignon","Uzes","Nimes","Aigues Mortes","Saintes Maries de la mer","Collioure","Carcassonne","Ariege","Toulouse","Montauban","Biarritz","Bayonne","La Rochelle"]

    url_list = ['https://www.booking.com/searchresults.fr.html?aid=304142&ss={}&offset='.format(elt) for elt in list_cities]
    start_urls = []
    for elt in url_list:
        for i in range(0,25,25):
            start_urls.append(str(elt) + str(i))
    
    def start_requests(self):
        list_cities = ["Mont Saint Michel","St Malo","Bayeux","Le Havre","Rouen","Paris","Amiens","Lille","Strasbourg","Chateau du Haut Koenigsbourg","Colmar","Eguisheim","Besancon","Dijon","Annecy","Grenoble","Lyon","Gorges du Verdon","Bormes les Mimosas","Cassis","Marseille","Aix en Provence","Avignon","Uzes","Nimes","Aigues Mortes","Saintes Maries de la mer","Collioure","Carcassonne","Ariege","Toulouse","Montauban","Biarritz","Bayonne","La Rochelle"]
        n = 0
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse , meta ={'city' :list_cities[n] })
            n+=1


    


    def parse(self, response):
        rows = response.xpath("//div[@data-testid = 'property-card']")
      
        for row in rows:
            hotel_name = row.xpath('.//div[@data-testid = "title"]/text()').get()
            url_hotel = row.xpath('.//h3[@class = "a4225678b2"]/a/@href').get()
            #hotel_score = row.xpath('.//div[@class = "b5cd09854e d10a6220b4"]/@aria-label').extract()[0]
            hotel_score = row.xpath('.//div[@class = "b5cd09854e d10a6220b4"]/text()').get()
            city = response.request.meta['city']
            #url_next = response.xpath()

            yield response.follow(url= url_hotel, callback=self.parse_hotel, meta={'hotel_name': hotel_name, 'hotel_score': hotel_score, 'url_hotel': url_hotel, 'city':city})
        

    def parse_hotel(self, response):
        url_hotel = response.request.meta['url_hotel']
        hotel_name = response.request.meta['hotel_name']
        hotel_score = response.request.meta['hotel_score']
        city = response.request.meta['city']
        coord = response.xpath('/html/body/script[26]/text()').get()
        lat = float((coord.split(' ')[2].split(';'))[0])
        lon = float((coord.split(' ')[4].split(';'))[0])
        description = ''
        for row in response.xpath('//div[@id = "property_description_content"]/p'):

            description += str((row.xpath('.//text()').get()))
        yield {
                'hotel_name': hotel_name,
                'lat': lat,
                'lon': lon,
                'description': description,
                'hotel_score': hotel_score,
                'url_hotel': url_hotel,
                'city': city
                
            }


process = CrawlerProcess( {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36',
    #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    #'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    #'LOG_LEVEL': logging.INFO,
    "FEEDS": {
       "hotel" : {"format": "csv"},
    }
})


process.crawl(Booking_data)
process.start()
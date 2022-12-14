import scrapy
from scrapy.crawler import CrawlerProcess
import logging


class Booking_data(scrapy.Spider):
    name = 'booking_data'
    #allowed_domains = ['https://www.booking.com/']
    list_cities = ["Mont Saint Michel","St Malo","Bayeux","Le Havre","Rouen","Paris","Amiens","Lille","Strasbourg","Chateau du Haut Koenigsbourg","Colmar","Eguisheim","Besancon","Dijon","Annecy","Grenoble","Lyon","Gorges du Verdon","Bormes les Mimosas","Cassis","Marseille","Aix en Provence","Avignon","Uzes","Nimes","Aigues Mortes","Saintes Maries de la mer","Collioure","Carcassonne","Ariege","Toulouse","Montauban","Biarritz","Bayonne","La Rochelle"]
    url_list = ['https://www.booking.com/searchresults.fr.html?aid=304142&ss={}&offset='.format(elt) for elt in list_cities]
    print('ok1')
    start_urls = []
    for elt in url_list:
        for i in range(0,50,25):
            start_urls.append(str(elt) + str(i))
    print(start_urls)
    #start_urls = ['https://www.booking.com/searchresults.fr.html?aid=304142&ss={}&offset='.format(i) for i in range(0,25,25)]
    def start_requests(self):
        print('ok')
        for url in self.start_urls:
            print(url)
            yield scrapy.Request(url, self.parse)

    


    def parse(self, response):
        rows = response.xpath("//div[@data-testid = 'property-card']")
      
        for row in rows:
            hotel_name = row.xpath('.//div[@data-testid = "title"]/text()').get()
            url_hotel = row.xpath('.//h3[@class = "a4225678b2"]/a/@href').get()
            #hotel_score = row.xpath('.//div[@class = "b5cd09854e d10a6220b4"]/@aria-label').extract()[0]
            hotel_score = row.xpath('.//div[@class = "b5cd09854e d10a6220b4"]/text()').get()
            
            #url_next = response.xpath()

            yield response.follow(url= url_hotel, callback=self.parse_hotel, meta={'hotel_name': hotel_name, 'hotel_score': hotel_score, 'url_hotel': url_hotel})
        

    def parse_hotel(self, response):
        url_hotel = response.request.meta['url_hotel']
        hotel_name = response.request.meta['hotel_name']
        hotel_score = response.request.meta['hotel_score']

        coord = response.xpath('/html/body/script[26]/text()').get()
        lat = float((coord.split(' ')[2].split(';'))[0])
        lon = float((coord.split(' ')[4].split(';'))[0])
        description = ''
        for row in response.xpath('/html/body/div[3]/div/div[4]/div[1]/div[1]/div/div[5]/div/div/div[1]/div[1]/div[1]/div[1]/div[3]/p'):

            description += str((row.xpath('.//text()').get()))
        #print(hotel_name)
        
        yield {
                'hotel_name': hotel_name,
                'lat': lat,
                'lon': lon,
                'description': description,
                'hotel_score': hotel_score,
                'url_hotel': url_hotel
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
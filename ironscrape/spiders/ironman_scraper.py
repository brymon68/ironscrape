import scrapy
import urlparse
from urllib import urlencode

from ironscrape.items import IronScrapeItem

class ironman_scraper(scrapy.Spider):

    name = "ironscrape"
    allowed_domains = ["track.ironman.com"]
    start_urls = []

    races = ['joenkoeping', 'lakeplacid', 'wisconsin', 'germany', 'malaysia', 'worldchampionship', 'florida', 'newzealand',
             'arizona', 'australia', 'canada', 'switzerland', 'austria', 'coeurdalene', 'france', 'eagleman', 'brazil', 'japan',
             'westernaustralia', 'uk', 'lanzarote', 'louisville', 'southafrica', 'cozumel', 'texas', 'regensburg', 'wales', 'melbourne',
             'st.george', 'uschampionship', 'monttremblant', 'kalmar', 'loscabos', 'copenhagen', 'boulder', 'laketahoe', 'chattanooga',
             'maryland', 'fortaleza', 'copenhagen', 'vineman', 'taiwan70.3', 'steelhead70.3', 'lakestevens70.3', 'austria70.3', 'florida70.3',
             'monaco70.3', 'brazil70.3', 'stcroix70.3', 'honu70.3', 'california70.3', 'southafrica70.3', 'worldchampionship70.3', 'germany70.3', 'buffalosprings70.3',
             'geelong70.3', 'rhodeisland70.3', 'kansas70.3', 'muskoka70.3', 'singapore70.3', 'china70.3', 'neworleans70.3', 'calgary70.3', 'augusta70.3',
             'philippines70.3', 'timberman70.3', 'texas70.3', 'vineman70.3', 'boise70.3', 'mooseman70.3', 'boulder70.3', 'racine70.3',
             'miami70.3', 'longhorn70.3', 'branson70.3', 'cozumel70.3', 'japan70.3', 'syracuse70.3', 'mallorca70.3', 'busselton70.3',
             'portmacquarie70.3', 'sanjuan70.3', 'muncie70.3', 'italy70.3', 'switzerland70.3', 'yeppoon70.3', 'pocono70.3', 'france70.3',
             'srilanka70.3', 'panama70.3', 'uk70.3', 'cairns70.3', 'haugesund70.3', 'ireland70.3', 'salzburg70.3', 'phuket70.3', 'mandura70.3',
             'auckland70.3', 'stgeorge70.3', 'sunshinecoast70.3', 'luxembourg70.3', 'putrajaya70.3', 'monterrey70.3', 'aarhus70.3', 'victoria70.3',
             'fozdoiguacu70.3', 'silverman70.3', 'princeton70.3', 'kronborg70.3', 'ruegen70.3', 'sydney70.3', 'subicbay70.3', 'chattanooga70.3',
             'barcelona70.3', 'vietnam70.3', 'staffordshire70.3', 'kraichgau70.3', 'dublin70.3', 'santacruz70.3', 'vichy70.3', 'bintan70.3',
             'budapest70.3', 'korea70.3', 'riodejaneiro70.3', 'superfrog70.3', 'pula70.3', 'turkey70.3', 'pucon70.3', 'ballarat70.3', 'taupo70.3',
             'dubai70.3', 'uruguay70.3', 'bahrain70.3', 'buenosaires70.3', 'durban70.3', 'busan70.3', '5150zurich', '5150warsaw', '5150kraichgau',
             'kraichgau70.3', 'timbermansprint']
    years = ['2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016']

    # for i in range(1, 3001):
    #     for y in len(years):
    #         for r in len(races):
    #             params = {'year': years[y], 'race': races[r]}
    #             url = "http://track.ironman.com/newsearch.php?"
    #             url_parts = list(urlparse.urlparse(url))
    #             query = dict(urlparse.parse_qsl(url_parts[4]))
    #             query.update(params)
    #             url_parts[4] = urlencode(query)
    #             start_urls.append(urlparse.urlunparse(url_parts))

    for i in range(1,2):
        params = {'bib': i, 'rid': 727828834329}
        url = "http://track.ironman.com/newathlete.php?"
        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        start_urls.append(urlparse.urlunparse(url_parts))

    def parse(self, response):

        item = IronScrapeItem()
        swimDetails = {}
        summaryCount = 0
        genInfoCount = 0
        for sel in response.xpath('//div[@id="div-rank"]/text()').extract():
            item['overallRank'] = sel
        for sel in response.xpath('//div[@id="rank"]/text()').extract():
            item['divRank'] = sel
        for sel in response.xpath('//h1/text()').extract():
            item['athleteName'] = sel
        splitTables = response.xpath('//div[@class="athlete-table-details"]')
        splitsCount=0
        # for td in splitTables.xpath('//td/strong/text()'):
        #     if splitsCount == 13:
        #
        #     splitCount=splitsCount+1
        athleteTimes = response.xpath('//table[@id="athelete-details"]/tbody/tr/td/text()').extract()
        for i in athleteTimes:
            if summaryCount ==0:
                item['swimTime'] = i
                summaryCount=summaryCount+1
            elif summaryCount == 1:
                item['bikeTime'] = i
                summaryCount=summaryCount+1
            elif summaryCount == 2:
                item['runTime'] = i
                summaryCount=summaryCount+1
            elif summaryCount == 3:
                item['totalTime'] = i
        # swimDetailsList = response.xpath('//table[@id="general-info"]/tbody/tr/td/text()').extract()
        
        
        generalAthleteInfo = response.xpath('//table[@id="general-info"]/tbody/tr/td/text()').extract()
        for i in generalAthleteInfo:
            if genInfoCount ==0:
                item['bib'] = i
                genInfoCount=genInfoCount+1
            elif genInfoCount == 1:
                item['division'] = i
                genInfoCount=genInfoCount+1
            elif genInfoCount == 2:
                item['state'] = i
                genInfoCount=genInfoCount+1
            elif genInfoCount == 3:
                item['country'] = i
                genInfoCount=genInfoCount+1
        # yield item
    def getSplits(self, response, item):
        
        
import scrapy
import urlparse
from urllib import urlencode
import json
from json import JSONEncoder
import logging

from ironscrape.items import IronScrapeItem

logging.basicConfig(filename='ironscrape.log',level=logging.DEBUG)


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

    for i in range(1,50):
        params = {'bib': i, 'rid': 727828834329}
        url = "http://track.ironman.com/newathlete.php?"
        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        start_urls.append(urlparse.urlunparse(url_parts))


    def parse(self, response):
        item = IronScrapeItem()
        self.setSplits(response, item)
        self.setGeneralTimes(response, item)
        self.setGeneralInfo(response, item)
        yield item

    def setSplits(self, response, item):
        swimSplitsList=[]
        bikeSplitsList = []
        runSplitsList = []
        splitTables = response.xpath('//div[@class="athlete-table-details"]')
        splitCount=0
        splitData = splitTables.xpath('//td//text()').extract()
        swimSplitVals=[]
        bikeSplitVals1 =[]
        bikeSplitVals2 = []
        bikeSplitVals3 = []
        bikeSplitVals4 = []
        runSplitVals1=[]
        runSplitVals2=[]
        runSplitVals3=[]
        runSplitVals4=[]
        runSplitVals5=[]
        count=0
        if len(splitData) == 83:
            for td in splitData:
                if splitCount==12:
                    swimSplitVals.append(td)
                if splitCount==14:
                    bikeSplitVals1.append(td)
                    bikeSplitVals2.append(td)
                    bikeSplitVals3.append(td)
                    bikeSplitVals4.append(td)
                if splitCount==16:
                    runSplitVals1.append(td)
                    runSplitVals2.append(td)
                    runSplitVals3.append(td)
                    runSplitVals4.append(td)
                    runSplitVals5.append(td)
                elif splitCount in range(20, 28):
                    swimSplitVals.append(td)
                #here is bike splits now
                elif splitCount in range (28, 33):
                    bikeSplitVals1.append(td)
                elif splitCount in range (33, 38):
                    bikeSplitVals2.append(td)
                elif splitCount in range (38, 43):
                    bikeSplitVals3.append(td)
                elif splitCount in range (43, 51):
                    bikeSplitVals4.append(td)
                elif splitCount in range (51, 56):
                    runSplitVals1.append(td)
                elif splitCount in range (56, 61):
                    runSplitVals2.append(td)
                elif splitCount in range (61, 66):
                    runSplitVals3.append(td)
                elif splitCount in range (66, 71):
                    runSplitVals4.append(td)
                elif splitCount in range (71, 79):
                    runSplitVals5.append(td)
                else:
                    pass
                splitCount+=1
                count+=1
            try:
                swimSplit = SplitInfo(swimSplitVals[0], swimSplitVals[1], swimSplitVals[2], swimSplitVals[3], swimSplitVals[4], swimSplitVals[5], swimSplitVals[6], swimSplitVals[7], swimSplitVals[8])
                bikeSplit1 = SplitInfo(bikeSplitVals1[0], bikeSplitVals1[1], bikeSplitVals1[2], bikeSplitVals1[3], bikeSplitVals1[4], bikeSplitVals1[5], "", "", "")
                bikeSplit2 = SplitInfo(bikeSplitVals2[0], bikeSplitVals2[1], bikeSplitVals2[2], bikeSplitVals2[3], bikeSplitVals2[4], bikeSplitVals2[5], "", "", "")
                bikeSplit3 = SplitInfo(bikeSplitVals3[0], bikeSplitVals3[1], bikeSplitVals3[2], bikeSplitVals3[3], bikeSplitVals3[4], bikeSplitVals3[5], "", "", "")
                bikeSplit4 = SplitInfo(bikeSplitVals4[0], bikeSplitVals4[1], bikeSplitVals4[2], bikeSplitVals4[3], bikeSplitVals4[4], bikeSplitVals4[5], bikeSplitVals4[6], bikeSplitVals4[7], bikeSplitVals4[8])
                runSplit1 = SplitInfo(runSplitVals1[0], runSplitVals1[1], runSplitVals1[2], runSplitVals1[3], runSplitVals1[4], runSplitVals1[5], "", "", "")
                runSplit2 = SplitInfo(runSplitVals2[0], runSplitVals2[1], runSplitVals2[2], runSplitVals2[3], runSplitVals2[4], runSplitVals2[5], "", "", "")
                runSplit3 = SplitInfo(runSplitVals3[0], runSplitVals3[1], runSplitVals3[2], runSplitVals3[3], runSplitVals3[4], runSplitVals3[5], "", "", "")
                runSplit4 = SplitInfo(runSplitVals4[0], runSplitVals4[1], runSplitVals4[2], runSplitVals4[3], runSplitVals4[4], runSplitVals4[5], "", "", "")
                runSplit5 = SplitInfo(runSplitVals5[0], runSplitVals5[1], runSplitVals5[2], runSplitVals5[3], runSplitVals5[4], runSplitVals5[5], runSplitVals5[6], runSplitVals5[7], runSplitVals5[8])
                logging.info("Successfully inserted <TD> data into lists for: "+response.url)
            except:
                logging.info("WARNING: Unable to insert <TD> data into list on url: "+response.url)
                exit()

            jsonFormat1 = JSONEncoder().encode(swimSplit.returnDictionary())
            jsonFormat2 = JSONEncoder().encode(bikeSplit1.returnDictionary())
            jsonFormat3 = JSONEncoder().encode(bikeSplit2.returnDictionary())
            jsonFormat4 = JSONEncoder().encode(bikeSplit3.returnDictionary())
            jsonFormat5 = JSONEncoder().encode(bikeSplit4.returnDictionary())
            jsonFormat6 = JSONEncoder().encode(runSplit1.returnDictionary())
            jsonFormat7 = JSONEncoder().encode(runSplit2.returnDictionary())
            jsonFormat8 = JSONEncoder().encode(runSplit3.returnDictionary())
            jsonFormat9 = JSONEncoder().encode(runSplit4.returnDictionary())
            jsonFormat10 = JSONEncoder().encode(runSplit5.returnDictionary())

            swimSplitsList.append(jsonFormat1)
            bikeSplitsList.append(jsonFormat2)
            bikeSplitsList.append(jsonFormat3)
            bikeSplitsList.append(jsonFormat4)
            bikeSplitsList.append(jsonFormat5)
            runSplitsList.append(jsonFormat6)
            runSplitsList.append(jsonFormat7)
            runSplitsList.append(jsonFormat8)
            runSplitsList.append(jsonFormat9)
            runSplitsList.append(jsonFormat10)
            item['swimDetails'] = swimSplitsList
            item['bikeDetails'] = bikeSplitsList
            item['runDetails'] = runSplitsList
            logging.info("successful")

    def setGeneralTimes(self, response, item):
        generalTimesCount = 0
        athleteTimes = response.xpath('//table[@id="athelete-details"]/tbody/tr/td/text()').extract()
        for i in athleteTimes:
            if generalTimesCount ==0:
                item['swimTime'] = i
                generalTimesCount +=1
            elif generalTimesCount == 1:
                item['bikeTime'] = i
                generalTimesCount+=1
            elif generalTimesCount == 2:
                item['runTime'] = i
                generalTimesCount+=1
            elif generalTimesCount == 3:
                item['totalTime'] = i

    def setGeneralInfo(self, response, item):
        genInfoCount = 0
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
        for sel in response.xpath('//div[@id="div-rank"]/text()').extract():
            item['overallRank'] = sel
        for sel in response.xpath('//div[@id="rank"]/text()').extract():
            item['divRank'] = sel
        for sel in response.xpath('//h1/text()').extract():
            item['athleteName'] = sel


class SplitInfo():
    def __init__(self, type, name, distance, splitTime, raceTime, pace, divisionRank, genderRank, overallRank):

        self.type = type
        self.name = name
        self.distance = distance
        self.splitTime = splitTime
        self.raceTime = raceTime
        self.pace=pace
        self.divisionRank =divisionRank
        self.genderRank = genderRank
        self.overallRank =overallRank

    def returnDictionary(self):
        dictionary = {"type": self.type, "ranks": {"divisionRank":self.divisionRank, "genderRank":self.genderRank, "overallRank":self.overallRank}, "name":self.name, "distance":self.distance, "splitTime":self.splitTime, "raceTime":self.raceTime, "pace":self.pace }
        return dictionary
        
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


    for i in range(1,2):
        params = {'bib': i, 'rid': 727828834324}
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
        splitTables = response.xpath('//div[@class="athlete-table-details"]')
        splitData = splitTables.xpath('//td//text()').extract()
        self.processSwimSplits(splitData, item)
        self.processBikeSplits(splitData, item)
        self.processRunSplits(splitData, item)



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

    def processSwimSplits(self, splitdata, item):
        swimSplitsList=[]
        swimSplitVals=[]
        splitCount = 0
        count = 0
        for td in splitdata:
            if splitCount == 12:
                swimSplitVals.append(td)
            elif splitCount in range(20, 28):
                swimSplitVals.append(td)
            else:
                pass
            splitCount += 1
            count += 1
        try:
            obj = SplitInfo(swimSplitVals[0], swimSplitVals[1], swimSplitVals[2], swimSplitVals[3], swimSplitVals[4], swimSplitVals[5], swimSplitVals[6], swimSplitVals[7], swimSplitVals[8])
            jsonFormat = JSONEncoder().encode(obj.returnDictionary())
            swimSplitsList.append(jsonFormat)
            item['swimDetails'] = swimSplitsList
        except:
            print "whoa some shit when wrong in swim"


    def processBikeSplits(self, splitdata, item):
        bikeSplitsJSONList = []
        bikeSplitsList = []
        for i in range(4):
            bikeSplitsList.append([])
        splitCount = 0
        count = 0
        if (len(splitdata) == 83) or (len(splitdata) == 87) or (len(splitdata) ==88):
            for td in splitdata:
                if splitCount == 14:
                    for list in bikeSplitsList:
                        list.append(td)
                elif splitCount in range(28, 33):
                    bikeSplitsList[0].append(td)
                elif splitCount in range(33, 38):
                    bikeSplitsList[1].append(td)
                elif splitCount in range(38, 43):
                    bikeSplitsList[2].append(td)
                elif splitCount in range(43, 48):
                    bikeSplitsList[3].append(td)
                elif splitCount in range(48, 51):
                    for list in bikeSplitsList:
                        list.append(td)
                else:
                    pass
                splitCount += 1
                count += 1
        try:
            for list in bikeSplitsList:
                splitinfo = SplitInfo(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8])
                jsonFormat = JSONEncoder().encode(splitinfo.returnDictionary())
                bikeSplitsJSONList.append(jsonFormat)
            item['bikeDetails'] = bikeSplitsJSONList
        except:
            print "whoa some shit when wrong in bike"

    def processRunSplits(self, splitdata, item):
        runSplitsJSONList = []
        runSplitsList = []
        splitCount = 0
        count = 0
        if len(splitdata) == 83:
            for y in range(5):
                runSplitsList.append([])
            for td in splitdata:
                if splitCount == 16:
                    for list in runSplitsList:
                        list.append(td)
                elif splitCount in range(51, 56):
                    runSplitsList[0].append(td)
                elif splitCount in range(56, 61):
                    runSplitsList[1].append(td)
                elif splitCount in range(61, 66):
                    runSplitsList[2].append(td)
                elif splitCount in range(66, 71):
                    runSplitsList[3].append(td)
                elif splitCount in range(71, 76):
                    runSplitsList[4].append(td)
                elif splitCount in range (76, 79):
                    for list in runSplitsList:
                        list.append(td)
                else:
                    pass
                splitCount += 1
                count += 1
        elif len(splitdata) == 87 or len(splitdata) ==88:
            for y in range(6):
                runSplitsList.append([])
            for td in splitdata:
                if splitCount == 16:
                    for list in runSplitsList:
                        list.append(td)
                elif splitCount in range(51, 56):
                    runSplitsList[0].append(td)
                elif splitCount in range(56, 61):
                    runSplitsList[1].append(td)
                elif splitCount in range(61, 66):
                    runSplitsList[2].append(td)
                elif splitCount in range(66, 71):
                    runSplitsList[3].append(td)
                elif splitCount in range(71, 76):
                    runSplitsList[4].append(td)
                elif splitCount in range(76, 81):
                    runSplitsList[5].append(td)
                elif splitCount in range(81, 84):
                    for list in runSplitsList:
                        list.append(td)
                else:
                    pass
                splitCount += 1
                count += 1
        try:
            for list in runSplitsList:
                splitinfo = SplitInfo(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8])
                jsonFormat = JSONEncoder().encode(splitinfo.returnDictionary())
                runSplitsJSONList.append(jsonFormat)
            item['runDetails'] = runSplitsJSONList
        except:
            print "whoa some shit when wrong in run"


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
        
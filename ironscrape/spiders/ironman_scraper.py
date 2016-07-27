import scrapy
import urlparse
from urllib import urlencode
import json
from json import JSONEncoder
import logging
import re
import math

from ironscrape.items import IronScrapeItem

logging.basicConfig(filename='ironscrape.log',level=logging.DEBUG)


class ironman_scraper(scrapy.Spider):

    name = "ironscrape"
    allowed_domains = ["track.ironman.com"]
    start_urls = []


    for i in range(27,28):
        params = {'bib': i, 'rid': 727828834326}
        url = "http://track.ironman.com/newathlete.php?"
        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        start_urls.append(urlparse.urlunparse(url_parts))


    def parse(self, response):
        splitTables = response.xpath('//div[@class="athlete-table-details"]')
        splitdata = splitTables.xpath('//td//text()').extract()
        if len(splitdata) > 0:
            item = IronScrapeItem()
            splits = self.processor(response)
            self.setGeneralTimes(response, item)
            self.setGeneralInfo(response, item)
            self.processSplits(splits, item)
            yield item
        else:
            logging.info("Page contains no td values. URL is: "+str(response.url))

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

    def processor(self, response):
        splitsLists=[[], [], []]
        data = response.xpath('//body//text()').extract()
        filteredList = []
        edgePositions=[]
        edgeCount=0
        otherDataCount = 0
        for y in data:
            if re.search('[a-zA-Z0-9]', y):
                filteredList.append(y)
        for edge in filteredList:
            if edge == "Overall Rank":
                edgePositions.append(edgeCount+1)
                edgeCount+=1
            elif edge == "BIKE DETAILS ":
                edgePositions.append(edgeCount)
                edgeCount+=1
            elif edge == "Transition Details":
                edgePositions.append(edgeCount)
                edgeCount+=1
            elif edge == "RUN DETAILS ":
                edgePositions.append(edgeCount)
                edgeCount+=1
            else:
                edgeCount+=1
        for g in filteredList:
            if otherDataCount in range(edgePositions[0], edgePositions[1]):
                splitsLists[0].append(g)
                otherDataCount+=1
            elif otherDataCount in range (edgePositions[2], edgePositions[3]):
                splitsLists[1].append(g)
                otherDataCount+=1
            elif otherDataCount in range (edgePositions[4], edgePositions[5]):
                splitsLists[2].append(g)
                otherDataCount+=1
            else:
                otherDataCount+=1
        return splitsLists

    def processSplits(self, splits, item):
        swimSplitsJSONList=[]
        bikeSplitsJSONList=[]
        runSplitsJSONList=[]

        count=0
        for set in splits:
            newSet = set[:-3]
            new = []
            for i in range(0, len(newSet), 5):
                new.append(newSet[i : i+5])
            for i in new:
                i.append(set[-3])
                i.append(set[-2])
                i.append(set[-1])
                if count ==0:
                    splitInfo = SplitInfo("swim", i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
                    swimSplitsJSONList.append(splitInfo.returnDictionary())
                if count ==1:
                    splitInfo = SplitInfo("bike", i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
                    bikeSplitsJSONList.append(splitInfo.returnDictionary())
                if count ==2:
                    splitInfo = SplitInfo("run", i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
                    runSplitsJSONList.append(splitInfo.returnDictionary())
            count+=1
        item['swimDetails'] = swimSplitsJSONList
        item['bikeDetails'] = bikeSplitsJSONList
        item['runDetails'] = runSplitsJSONList



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
        
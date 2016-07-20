# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class IronScrapeItem(scrapy.Item):
    raceName = scrapy.Field()
    raceYear = scrapy.Field()
    athleteName = scrapy.Field()
    swimTime = scrapy.Field()
    bikeTime = scrapy.Field()
    runTime = scrapy.Field()
    totalTime = scrapy.Field()
    divRank = scrapy.Field()
    overallRank = scrapy.Field()
    bib = scrapy.Field()
    division = scrapy.Field()
    country = scrapy.Field()
    state = scrapy.Field()
    swimDetails = scrapy.Field()
    bikeDetails = scrapy.Field()
    runDetails = scrapy.Field()
    t1Transition = scrapy.Field()
    t2Transition = scrapy.Field()



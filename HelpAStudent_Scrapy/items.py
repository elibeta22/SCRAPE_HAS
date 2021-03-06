# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy


class HelpAStudentItem(scrapy.Item):
    school_name = scrapy.Field()
    school_professors = scrapy.Field()

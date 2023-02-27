import scrapy

class IlpostItem(scrapy.Item):
    topic = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()

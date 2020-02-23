import scrapy


class Concert(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field(serializer=str)
    country = scrapy.Field()
    city = scrapy.Field()
    venue = scrapy.Field()
    bands = scrapy.Field()

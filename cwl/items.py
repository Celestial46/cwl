import scrapy
from itemadapter import ItemAdapter

class CwlItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    status = scrapy.Field()
    content_type = scrapy.Field()
    scraped_at = scrapy.Field()

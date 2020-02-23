from datetime import datetime

import scrapy

from crawler.items import Concert


class MastersofrockSpider(scrapy.Spider):
    name = 'mastersofrock'
    allowed_domains = ['mastersofrock.cz']
    start_urls = ['https://www.mastersofrock.cz/en/koncerty']

    def parse(self, response):
        events = response.xpath('//div[@class="card band-item"]')

        for event in events:
            url = event.css('div.item__info > h4 > a::attr(href)').extract_first()
            name = event.css('div.item__info > h4 > a::text').extract_first().strip()
            date, location = [x.strip() for x in event.css('div.item__info > span.date::text').extract()]
            loc = location.split(' - ')
            venue, city = loc[0], loc[-1]

            yield Concert(
                url=url,
                name=name,
                date=datetime.strptime(date, '%d.%m.%Y %H:%M').date(),
                country='Czech Republic',
                city=city,
                venue=venue,
                bands=[],
            )

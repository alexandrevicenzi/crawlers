from datetime import datetime

import scrapy

from crawler.items import Concert


class RisingHornsSpider(scrapy.Spider):
    name = 'risinghorns'
    allowed_domains = ['risinghorns.com']
    start_urls = ['https://www.risinghorns.com/upcoming-festivals/']

    def parse(self, response):
        events = response.xpath('//table[@id="tablepress-2"]//tbody//tr')

        for event in events:
            url = event.xpath('td[1]//a//@href').extract_first()
            name = event.xpath('td[1]//a//text()').extract_first()
            date = event.xpath('td[2]//text()').extract_first()
            # duration = event.xpath('td[4]//text()').extract_first()
            country = event.xpath('td[3]//text()').extract_first()
            # genre = event.xpath('td[7]//text()').extract_first()

            yield Concert(
                url=url,
                name=name,
                date=datetime.strptime(date, '%d/%m/%Y').date(),
                country=country,
                city=None,
                venue=None,
                bands=[],
            )

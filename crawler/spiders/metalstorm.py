from datetime import datetime

import scrapy

from crawler.items import Concert


class MetalStormSpider(scrapy.Spider):
    name = 'metalstorm'
    allowed_domains = ['metalstorm.net']
    start_urls = ['http://www.metalstorm.net/events/events.php']

    def parse(self, response):
        events = response.css('div[id="page-content"]').xpath('//table[@class="table table-striped break-on-xs"]/tr')

        for event in events[1:]:
            url = response.urljoin(event.xpath('td[2]/a/@href').extract_first())
            name = event.xpath('td[2]/b/a/text()').extract_first()
            date = event.xpath('td[2]/span/text()').extract_first()
            country = event.xpath('td[3]/a[1]/text()').extract_first()
            city = event.xpath('td[3]/a[2]/text()').extract_first()
            venue = event.xpath('td[3]/span/text()').extract_first()
            bands = event.xpath('td[4]//text()').extract()
            # audience = event.xpath('td[5]/text()').extract_first()
            # event_type = event.xpath('td[6]/text()').extract_first()

            date = date.split('-')[0]

            yield Concert(
                url=url,
                name=name,
                date=datetime.strptime(date, '%d.%m.%Y').date(),
                country=country,
                city=city,
                venue=venue,
                bands=bands,
            )

        next_page = response.xpath('//ul[@class="pagination"]/li[@class="active"]/following-sibling::li/a/@href').extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

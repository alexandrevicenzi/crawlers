from datetime import datetime

import scrapy

from crawler.items import Concert


class MelodkaSpider(scrapy.Spider):
    name = 'melodka'
    allowed_domains = ['melodka.cz']
    start_urls = ['https://www.melodka.cz/program/']

    def parse(self, response):
        events = response.xpath('//div[@id="program_panel"]//div[contains(@class, "program_line2")]')

        for event in events:
            url = response.urljoin(event.css('div.nazev > a::attr(href)').extract_first())
            event_type = event.css('div::attr(title)').extract_first()

            if event_type != 'Live koncert':
                continue

            name = event.css('div.nazev > a::text').extract_first()
            date = event.css('div.datum::text').extract_first()

            yield Concert(
                url=url,
                name=name,
                date=datetime.strptime(date, '%d. %m. %Y').date(),
                country='Czech Republic',
                city='Brno',
                venue='Melodka',
                bands=[],
            )

        next_page = response.xpath('//div[@class="paginator"]//a[not(contains(@class, "nonactive"))]//following-sibling::a[@class="nonactive"]//@href').extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

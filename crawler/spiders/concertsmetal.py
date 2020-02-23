from datetime import datetime

import scrapy

from crawler.items import Concert


class ConcertsMetalSpider(scrapy.Spider):
    name = 'concertsmetal'
    allowed_domains = ['concerts-metal.com']
    start_urls = ['https://en.concerts-metal.com/search.php']

    def parse(self, response):
        events = response.xpath('//div[@class="row"][1]//div[@class="card mb-3 shadow-sm"]')

        for event in events:
            try:
                url = response.urljoin(event.xpath('//h6//a//@href').extract_first())
                name = event.xpath('//h6//text()').extract_first()
                _, date_duration, country_city = event.css('::text').extract()
            except:
                # This website is just bad, skip if failing
                continue

            parts = country_city.split(' - ')

            if len(parts) == 2:
                country, city = parts[0], parts[1]
            else:
                country, city = parts[0], parts[-1]

            if len(date_duration) > 10:
                date = date_duration[:10]
            else:
                date = date_duration

            yield Concert(
                url=url,
                name=name,
                date=datetime.strptime(date, '%d/%m/%Y').date(),
                country=country.strip(),
                city=city.strip(),
                venue=None,
                bands=[],
            )

        next_page = response.xpath('//center//h2[contains(text(), "Next events")]//parent::center//following-sibling::center[1]//b//following-sibling::a[1]//@href').extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

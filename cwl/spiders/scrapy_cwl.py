import scrapy
from urllib.parse import urljoin, urlparse

class FullSiteSpider(scrapy.Spider):
    name = "fullsite"
    start_urls = ["https://example.com"]
    visited_urls = set()

    def parse(self, response):
        self.visited_urls.add(response.url)
        title = response.xpath('//title/text()').get()
        text = ' '.join(response.xpath('//body//text()').getall()).strip()

        yield {
            "url": response.url,
            "title": title,
            "text": text,
        }

        for href in response.css('a::attr(href)').getall():
            full_url = urljoin(response.url, href)
            if self._is_valid_url(full_url) and full_url not in self.visited_urls:
                yield scrapy.Request(full_url, callback=self.parse)

    def _is_valid_url(self, url):
        domain = urlparse(self.start_urls[0]).netloc
        return urlparse(url).netloc == domain and url.startswith("http")

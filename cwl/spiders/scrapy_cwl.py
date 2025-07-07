import scrapy
from urllib.parse import urljoin, urlparse
import logging
from cwl.items import CwlItem

class FullSiteSpider(scrapy.Spider):
    name = "fullsite"
    start_urls = ["https://example.com"]
    visited_urls = set()
    
    # Spider settings
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 2,
        'DEPTH_LIMIT': 3,  # Limit depth to avoid infinite crawling
    }

    def __init__(self, *args, **kwargs):
        super(FullSiteSpider, self).__init__(*args, **kwargs)
        self.logger.setLevel(logging.INFO)

    def parse(self, response):
        try:
            self.visited_urls.add(response.url)
            
            # Extract title
            title = response.xpath('//title/text()').get()
            if not title:
                title = response.css('title::text').get()
            title = title.strip() if title else "No title"
            
            # Extract text content more carefully
            text_elements = response.xpath('//body//text()[normalize-space()]').getall()
            text = ' '.join([t.strip() for t in text_elements if t.strip()])
            
            # Log the extraction
            self.logger.info(f"Scraped: {response.url} - Title: {title[:50]}...")

            item = CwlItem()
            item['url'] = response.url
            item['title'] = title
            item['text'] = text[:1000]  # Limit text length
            item['status'] = response.status
            item['content_type'] = response.headers.get('Content-Type', b'').decode('utf-8')
            
            yield item

            # Extract and follow links
            links = response.css('a::attr(href)').getall()
            for href in links:
                if href:
                    full_url = urljoin(response.url, href)
                    if self._is_valid_url(full_url) and full_url not in self.visited_urls:
                        yield scrapy.Request(
                            full_url, 
                            callback=self.parse,
                            errback=self.handle_error,
                            dont_filter=False
                        )
        except Exception as e:
            self.logger.error(f"Error parsing {response.url}: {str(e)}")

    def _is_valid_url(self, url):
        try:
            parsed_start = urlparse(self.start_urls[0])
            parsed_url = urlparse(url)
            
            # Check if it's the same domain and is a valid HTTP URL
            return (parsed_url.netloc == parsed_start.netloc and 
                    url.startswith(("http://", "https://")) and
                    not url.endswith(('.pdf', '.jpg', '.jpeg', '.png', '.gif', '.css', '.js')))
        except Exception:
            return False

    def handle_error(self, failure):
        self.logger.error(f"Request failed: {failure.request.url} - {failure.value}")

    def closed(self, reason):
        self.logger.info(f"Spider closed: {reason}. Visited {len(self.visited_urls)} URLs.")

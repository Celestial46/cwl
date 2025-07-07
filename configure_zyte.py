#!/usr/bin/env python3
"""
ZYTE Configuration Helper

This script helps you configure ZYTE API for your Scrapy project.
Before running this script, make sure you have:
1. A ZYTE account with API access
2. Your ZYTE API key

Usage:
    python configure_zyte.py --api-key YOUR_API_KEY
"""

import sys
import argparse
import os
import re

def update_settings_with_zyte(api_key, settings_file="cwl/settings.py"):
    """Update settings.py with ZYTE configuration"""
    
    if not os.path.exists(settings_file):
        print(f"Error: {settings_file} not found!")
        return False
    
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # Replace the commented ZYTE configuration
    zyte_config = f'''# ZYTE API Configuration
ZYTE_API_KEY = '{api_key}'
ZYTE_API_URL = 'https://api.zyte.com/v1/extract'

DOWNLOADER_MIDDLEWARES.update({{
    'scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware': 1000,
}})

ZYTE_API_PROVIDER_PARAMS = {{
    'geolocation': 'US',
    'javascript': True,
    'screenshots': False,
}}'''
    
    # Find and replace the commented section
    pattern = r'# ZYTE API Configuration.*?# ZYTE_API_PROVIDER_PARAMS = \{.*?\}'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, zyte_config, content, flags=re.DOTALL)
    else:
        # If not found, append at the end
        content += '\n\n' + zyte_config
    
    with open(settings_file, 'w') as f:
        f.write(content)
    
    print(f"✅ ZYTE configuration updated in {settings_file}")
    return True

def create_zyte_spider(spider_name="zyte_spider"):
    """Create a spider optimized for ZYTE API"""
    
    spider_content = f'''import scrapy
from cwl.items import CwlItem

class {spider_name.title().replace('_', '')}Spider(scrapy.Spider):
    name = "{spider_name}"
    start_urls = ["https://example.com"]
    
    # Use ZYTE API for all requests
    custom_settings = {{
        'ZYTE_API_ENABLED': True,
        'CONCURRENT_REQUESTS': 5,
        'DOWNLOAD_DELAY': 0.5,
    }}

    def parse(self, response):
        """Parse the response using ZYTE API enhanced data"""
        
        item = CwlItem()
        item['url'] = response.url
        item['title'] = response.xpath('//title/text()').get() or "No title"
        item['text'] = ' '.join(response.xpath('//body//text()[normalize-space()]').getall()).strip()
        item['status'] = response.status
        item['content_type'] = response.headers.get('Content-Type', b'').decode('utf-8')
        
        yield item
        
        # Follow links if needed
        for href in response.css('a::attr(href)').getall():
            if href and href.startswith(('http://', 'https://')):
                yield scrapy.Request(href, callback=self.parse)
'''
    
    spider_file = f"cwl/spiders/{spider_name}.py"
    with open(spider_file, 'w') as f:
        f.write(spider_content)
    
    print(f"✅ ZYTE spider created: {spider_file}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Configure ZYTE API for Scrapy project')
    parser.add_argument('--api-key', required=True, help='Your ZYTE API key')
    parser.add_argument('--spider-name', default='zyte_spider', help='Name for the ZYTE spider')
    
    args = parser.parse_args()
    
    print("🔧 Configuring ZYTE API for your Scrapy project...")
    
    # Update settings
    if update_settings_with_zyte(args.api_key):
        print("✅ Settings updated successfully")
    else:
        print("❌ Failed to update settings")
        return 1
    
    # Create ZYTE spider
    if create_zyte_spider(args.spider_name):
        print("✅ ZYTE spider created successfully")
    else:
        print("❌ Failed to create ZYTE spider")
        return 1
    
    print("\n🎉 ZYTE configuration complete!")
    print(f"You can now run your ZYTE spider with:")
    print(f"    scrapy crawl {args.spider_name}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
'''

To use this script when you get your ZYTE API key:
python configure_zyte.py --api-key YOUR_ZYTE_API_KEY
'''

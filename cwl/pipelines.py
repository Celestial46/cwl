import datetime
from itemadapter import ItemAdapter

class CwlPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Add timestamp
        adapter['scraped_at'] = datetime.datetime.now().isoformat()
        
        # Clean and validate title
        if adapter.get('title'):
            adapter['title'] = adapter['title'].strip()
        
        # Clean text content
        if adapter.get('text'):
            adapter['text'] = ' '.join(adapter['text'].split())
            
        return item

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('scraped_data.jsonl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        import json
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item

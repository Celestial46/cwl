# CWL Scrapy Project

A web scraping project built with Scrapy, designed to work with ZYTE API for enhanced scraping capabilities.

## Features

- 🕷️ Full-site scraping with configurable depth limits
- 🔧 ZYTE API integration ready
- 📊 Structured data extraction with items and pipelines
- 🛡️ Robust error handling and logging
- 📁 JSON Lines output format
- ⚡ Auto-throttling and rate limiting
- 🚫 Robots.txt compliance

## Project Structure

```
cwl/
├── cwl/
│   ├── __init__.py
│   ├── items.py          # Data structure definitions
│   ├── pipelines.py      # Data processing pipelines
│   ├── settings.py       # Scrapy settings
│   └── spiders/
│       ├── __init__.py
│       └── scrapy_cwl.py # Main spider
├── configure_zyte.py     # ZYTE configuration helper
├── requirements.txt      # Python dependencies
├── scrapy.cfg           # Scrapy project configuration
└── README.md            # This file
```

## Installation

1. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Scraping

Run the spider with default settings:
```bash
scrapy crawl fullsite
```

### Limited Scraping (for testing)

Limit the number of pages scraped:
```bash
scrapy crawl fullsite -s CLOSESPIDER_PAGECOUNT=10
```

### Output Formats

Save to different formats:
```bash
# JSON Lines (default)
scrapy crawl fullsite -o output.jsonl

# JSON
scrapy crawl fullsite -o output.json

# CSV
scrapy crawl fullsite -o output.csv
```

## ZYTE Integration

### Setup ZYTE API

1. **Get your ZYTE API key** from your ZYTE dashboard
2. **Configure the project**:
   ```bash
   python configure_zyte.py --api-key YOUR_ZYTE_API_KEY
   ```
3. **Run with ZYTE**:
   ```bash
   scrapy crawl zyte_spider
   ```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'cwl'**
   - Make sure you're running from the project root directory
   - Check that the project structure is correct

2. **ZYTE API not working**
   - Verify your API key is correct
   - Check your ZYTE account has sufficient credits
   - Ensure `scrapy-zyte-api` is installed

### Debugging

Enable debug logging:
```bash
scrapy crawl fullsite -L DEBUG
```

## Dependencies

- `scrapy>=2.11.0` - Web scraping framework
- `scrapy-zyte-api>=0.13.0` - ZYTE API integration
- `lxml>=4.6.0` - XML/HTML parser
- `w3lib>=1.21.0` - Web utility functions
- `twisted>=22.4.0` - Networking engine
- `itemadapter>=0.8.0` - Item handling
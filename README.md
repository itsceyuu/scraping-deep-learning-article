# scraping-deep-learning-article
This project scrapes deep learning research articles from arXiv. It extracts metadata (title, authors, year, abstract, PDF URL) and saves article thumbnails.

## Architecture

- `scrap_ai/main.py` - Main scraping script using Selenium with Chrome WebDriver
- `data/articles.csv` - Output CSV with scraped article metadata
- `data/thumbnail/` - Screenshots of article entries from arXiv

## Configuration

The scraper can be configured by modifying these constants in `main.py`:
- `SEARCH_URL` - arXiv search query URL
- `MAX_ARTICLES` - Maximum number of articles to scrape (default: 20)
- `YEAR_MIN` - Minimum publication year filter (default: 2017)
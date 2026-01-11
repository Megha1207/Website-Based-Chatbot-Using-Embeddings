import sys
import json
from src.crawler import WebsiteCrawler
from config import CRAWL_OUTPUT_PATH

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Usage: python test_crawler.py <website_url>")

    url = sys.argv[1].strip()

    crawler = WebsiteCrawler(max_depth=1, max_pages=20)
    pages = crawler.crawl(url)

    with open(CRAWL_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)

    print(f" Crawl output saved to: {CRAWL_OUTPUT_PATH}")

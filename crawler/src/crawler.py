# src/crawler.py

import requests
import trafilatura
from bs4 import BeautifulSoup
from collections import deque
import hashlib
from datetime import datetime
from urllib.parse import urlparse

from config import (
    MAX_DEPTH,
    REQUEST_TIMEOUT,
    MIN_TEXT_LENGTH,
    MAX_PAGES,
    HEADERS,
    MAX_TEXT_LENGTH
)

from .utils import (
    validate_url,
    normalize_url,
    is_same_domain,
    clean_text,
    should_skip_url,
    canonicalize_url
)


class WebsiteCrawler:
    def __init__(self, max_depth=MAX_DEPTH, max_pages=MAX_PAGES):
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.visited = set()
        self.pages = []
        self.content_hashes = set()

    def crawl(self, start_url: str):
        if not validate_url(start_url):
            raise ValueError("Invalid URL")

        start_url = canonicalize_url(start_url)
        queue = deque([(start_url, 0)])

        while queue and len(self.pages) < self.max_pages:
            url, depth = queue.popleft()
            url = canonicalize_url(url)

            if url in self.visited or depth > self.max_depth:
                continue

            print(f"[CRAWLING] {url}")
            self.visited.add(url)

            try:
                response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
                if "text/html" not in response.headers.get("Content-Type", ""):
                    continue

                html = response.text

                # -------- Trafilatura extraction --------
                main_text = trafilatura.extract(
                    html,
                    include_comments=False,
                    include_tables=True,
                    favor_recall=True
                )

                metadata = trafilatura.extract_metadata(html)
                title = metadata.title if metadata and metadata.title else ""

                # -------- Fallback --------
                if not main_text:
                    soup = BeautifulSoup(html, "lxml")
                    title = soup.title.string.strip() if soup.title else ""
                    main_text = soup.get_text(separator=" ")

                # -------- Process content --------
                if main_text:
                    text = clean_text(main_text)

                    if len(text) > MAX_TEXT_LENGTH:
                        text = text[:MAX_TEXT_LENGTH]

                    if len(text) < MIN_TEXT_LENGTH:
                        continue

                    content_hash = hashlib.md5(text.encode("utf-8")).hexdigest()

                    if content_hash in self.content_hashes:
                        continue

                    self.content_hashes.add(content_hash)

                    parsed = urlparse(url)

                    self.pages.append({
                        "id": f"page_{len(self.pages)}",
                        "url": url,
                        "domain": parsed.netloc,
                        "title": title,
                        "text": text,
                        "text_length": len(text),
                        "depth": depth,
                        "crawled_at": datetime.utcnow().isoformat()
                    })

                # -------- Link discovery --------
                if depth < self.max_depth:
                    soup = BeautifulSoup(html, "lxml")
                    for link in soup.find_all("a", href=True):
                        next_url = canonicalize_url(normalize_url(url, link["href"]))

                        if (
                            is_same_domain(start_url, next_url)
                            and not should_skip_url(next_url)
                            and next_url not in self.visited
                        ):
                            queue.append((next_url, depth + 1))

            except Exception as e:
                print(f"[ERROR] {url} -> {e}")

        return self.pages

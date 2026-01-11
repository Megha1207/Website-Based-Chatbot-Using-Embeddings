import validators
from urllib.parse import urljoin, urlparse, urlunparse
import tldextract

from config import EXCLUDE_KEYWORDS, ALLOW_SUBDOMAIN, REQUIRE_WIKI_ARTICLE


# --------------------------------------------------
# URL validation
# --------------------------------------------------

def validate_url(url: str) -> bool:
    return validators.url(url)


# --------------------------------------------------
# URL normalization
# --------------------------------------------------

def normalize_url(base_url, link):
    return urljoin(base_url, link.split("#")[0])


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url)
    clean = parsed._replace(query="", fragment="")
    return urlunparse(clean)


# --------------------------------------------------
# Domain checks
# --------------------------------------------------

def is_same_domain(base_url, new_url):
    base = tldextract.extract(base_url)
    new = tldextract.extract(new_url)

    if ALLOW_SUBDOMAIN:
        return (base.domain, base.suffix) == (new.domain, new.suffix)
    else:
        return base.fqdn == new.fqdn


# --------------------------------------------------
# Crawl filtering (FIXED)
# --------------------------------------------------

def should_skip_url(url: str, start_url: str | None = None) -> bool:
    lower = url.lower()

    # 1️⃣ keyword blocks (safe for all sites)
    for keyword in EXCLUDE_KEYWORDS:
        if keyword.lower() in lower:
            return True

    # 2️⃣ Wikipedia-specific filtering ONLY for Wikipedia
    if REQUIRE_WIKI_ARTICLE and start_url:
        if "wikipedia.org" in start_url:
            parsed = urlparse(url)

            # must be a clean article
            if not parsed.path.startswith("/wiki/"):
                return True

            # block special namespaces
            if ":" in parsed.path.replace("/wiki/", ""):
                return True

    return False


# --------------------------------------------------
# Text cleaning
# --------------------------------------------------

def clean_text(text: str) -> str:
    return " ".join(text.split())

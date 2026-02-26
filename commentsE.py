import re
import time
import requests
import pandas as pd
from lxml import etree

# ================== CONFIG ==================
APP_URL = "https://apps.apple.com/us/app/meitu-ai-photo-video-editor/id416048305"
COUNTRY = "gb"          # United Kingdom App Store
MAX_PAGES = 10          # Apple public limit (~500 reviews)
OUTPUT_FILE = "meitu_gb_reviews.xlsx"
# ============================================


def extract_app_id(url_or_id: str) -> str:
    """
    Accepts either:
    - pure App ID (digits)
    - App Store URL containing idXXXXXXXX
    """
    s = url_or_id.strip()
    if s.isdigit():
        return s

    match = re.search(r"id(\d+)", s)
    if not match:
        raise ValueError("Cannot extract App ID from input.")
    return match.group(1)


def fetch_reviews_xml(app_id: str, country: str, page: int) -> bytes:
    """
    Fetch Apple iTunes customer reviews RSS feed (XML)
    """
    url = (
        f"https://itunes.apple.com/{country}/rss/customerreviews/"
        f"page={page}/id={app_id}/sortby=mostrecent/xml"
    )

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return response.content


def parse_reviews(xml_bytes: bytes):
    """
    Parse XML and extract:
    username, publish date, rating, title, review content
    """
    root = etree.fromstring(xml_bytes)

    namespaces = {
        "atom": "http://www.w3.org/2005/Atom",
        "im": "http://itunes.apple.com/rss",
    }

    rows = []

    for entry in root.findall("atom:entry", namespaces=namespaces):
        rating = entry.findtext("im:rating", namespaces=namespaces)
        if rating is None:
            continue  # Skip app metadata entry

        rows.append({
            "username": (
                entry.findtext("atom:author/atom:name", namespaces=namespaces) or ""
            ).strip(),
            "published_at": (
                entry.findtext("atom:updated", namespaces=namespaces)
                or entry.findtext("atom:published", namespaces=namespaces)
                or ""
            ).strip(),
            "rating": int(rating.strip()),
            "title": (
                entry.findtext("atom:title", namespaces=namespaces) or ""
            ).strip(),
            "content": (
                entry.findtext("atom:content", namespaces=namespaces) or ""
            ).strip(),
        })

    return rows


def main():
    app_id = extract_app_id(APP_URL)
    all_reviews = []

    for page in range(1, MAX_PAGES + 1):
        print(f"Fetching page {page}...")
        xml_data = fetch_reviews_xml(app_id, COUNTRY, page)
        reviews = parse_reviews(xml_data)

        if not reviews:
            break

        all_reviews.extend(reviews)
        time.sleep(0.3)  # be polite to Apple servers

    df = pd.DataFrame(all_reviews).drop_duplicates()
    #df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce", utc=True).dt.tz_convert(None)
    df.to_excel(OUTPUT_FILE, index=False)

    print(f"\nDone.")
    print(f"Total UK reviews fetched: {len(df)}")
    print(f"Saved to file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
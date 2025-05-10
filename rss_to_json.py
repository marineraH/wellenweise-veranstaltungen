
import feedparser
from datetime import datetime
import json
import re

rss_feeds = [
    "https://www.ostsee.de/veranstaltungen/rss.php",
    "https://www.kultur-mv.de/veranstaltungen/feed/",
    "https://www.kuenstlerort-ahrenshoop.de/veranstaltungen/feed/"
]

keywords = ["Lesung", "Kunst", "Wanderung", "Kochkurs", "Markt", "Ausstellung"]

def guess_location(title, link):
    if "kühlungsborn" in link.lower() or "kühlungsborn" in title.lower():
        return [54.1522, 11.7436]
    if "ahrenshoop" in link.lower() or "ahrenshoop" in title.lower():
        return [54.3876, 12.4386]
    if "königsstuhl" in title.lower() or "rügen" in title.lower():
        return [54.5672, 13.6611]
    if "rostock" in link.lower():
        return [54.0843, 12.1136]
    if "zingst" in title.lower():
        return [54.433, 12.7]
    return None

def parse_date(entry):
    try:
        return datetime(*entry.published_parsed[:3]).strftime("%Y-%m-%d")
    except:
        return None

events = []

for feed_url in rss_feeds:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        title = entry.title
        description = re.sub('<[^<]+?>', '', entry.get("description", ""))
        link = entry.link
        pub_date = parse_date(entry)
        relevant = any(kw.lower() in title.lower() or kw.lower() in description.lower() for kw in keywords)
        if relevant:
            events.append({
                "title": title,
                "start": pub_date,
                "description": description[:200],
                "url": link,
                "category": next((kw for kw in keywords if kw.lower() in title.lower() or kw.lower() in description.lower()), "Sonstiges"),
                "coordinates": guess_location(title, link)
            })

with open("events-geocoded.json", "w", encoding="utf-8") as f:
    json.dump(events, f, ensure_ascii=False, indent=2)

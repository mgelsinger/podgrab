#!/usr/bin/env python
"""
download_podcast.py  –  Download all episodes from a podcast RSS feed.

Usage:
    python download_podcast.py http://omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/A91018A4-EA4F-4130-BF55-AE270180C327/44710ECC-10BB-48D1-93C7-AE270180C33E/podcast.rss ./StuffYouShouldKnow
"""
import sys, os, re, html
import feedparser, requests
from tqdm import tqdm

def slugify(text):
    text = html.unescape(text)
    text = re.sub(r"[^\w\-_. ]", "", text)
    return "_".join(text.strip().split())

def download_feed(feed_url, outdir):
    os.makedirs(outdir, exist_ok=True)
    feed = feedparser.parse(feed_url)

    if feed.bozo:
        print("⚠️  Problem reading feed:", feed.bozo_exception)
        return

    print(f"Found {len(feed.entries)} entries in feed «{feed.feed.get('title','?')}»")

    for entry in reversed(feed.entries):          # oldest→newest
        title  = entry.get("title", "untitled")
        media  = entry.enclosures[0] if entry.enclosures else None
        if not media:
            print(f"❌  No enclosure for “{title}” – skipping")
            continue

        url  = media.href
        ext  = os.path.splitext(url.split("?")[0])[1] or ".mp3"
        date = entry.get("published_parsed") or entry.get("updated_parsed")
        prefix = f"{date.tm_year:04d}{date.tm_mon:02d}{date.tm_mday:02d}_" if date else ""
        filename = os.path.join(outdir, prefix + slugify(title) + ext)

        if os.path.exists(filename):
            print("✔️  Already have", filename)
            continue

        # Download with streaming + progress bar
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get("Content-Length", 0))
            bar   = tqdm(total=total, unit="B", unit_scale=True, desc=title[:40])
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bar.update(len(chunk))
            bar.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python download_podcast.py <feed_url> <output_dir>")
        sys.exit(1)
    download_feed(sys.argv[1], sys.argv[2])

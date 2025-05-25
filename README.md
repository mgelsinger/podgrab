
# 🎧 podgrab

*A tiny one-file Python utility to grab **every episode** from any podcast RSS feed.*

---
### Why?
I wanted a no-frills, scriptable way to archive entire podcast back-catalogues for personal listening—no ads removed (yet), no account sign-ups, and no heavyweight GUI apps.

---
## Features
- 💾 **Full-feed download** – iterates through every `<item>` in the RSS and saves the audio enclosure  
- 🚀 **Resumable** – skips files you already have, so you can re-run anytime  
- 🗂️ **Clean filenames** – `YYYYMMDD_Title.mp3` (customisable)  
- 📈 **Progress bar** – thanks to `tqdm`  
- 🔐 **Authenticated feeds** – works with premium URLs that include `user:token@`  
- 🐍 <100 lines of readable Python (3.8+)

---
## Requirements

| Package | Tested Version |
|---------|----------------|
| Python  | 3.8 – 3.12 |
| `feedparser` | ≥ 6.0 |
| `requests`   | ≥ 2.31 |
| `tqdm`       | ≥ 4.66 |

Install them in one go:

```
python -m pip install --upgrade feedparser requests tqdm
```

---
## Quick Start

```
# clone your repo (after you push this README 😉)
git clone https://github.com/yourname/podcast-downloader.git
cd podcast-downloader

# download every Stuff You Should Know episode
python download_podcast.py https://feeds.megaphone.fm/stuffyoushouldknow ./StuffYouShouldKnow
```

For Skeptoid’s **free** (latest-50) feed:

```
python download_podcast.py https://feed.skeptoid.com ./Skeptoid
```

Authenticated / premium feed (credentials embedded in URL):

```
python download_podcast.py https://USER:TOKEN@feed.skeptoid.com/premium.xml ./SkeptoidPremium
```

---
## Script Usage

```
python download_podcast.py <feed_url> <output_directory>
```

| Argument | Required | Description |
|----------|----------|-------------|
| `<feed_url>`        | ✅ | Full RSS URL (starts with `http` or `https`). |
| `<output_directory>` | ✅ | Where MP3/MP4 files are saved; created if missing. |

---
## How It Works (under the hood)
1. **Parse** the feed with `feedparser.parse()`.  
2. **Loop** through all entries (oldest → newest).  
3. **Grab** the first `<enclosure>` (audio).  
4. **Slugify** the episode title & prepend date.  
5. **Stream-download** via `requests`, updating a `tqdm` progress bar.  
6. **Skip** existing files to make the script idempotent.

---
## Customising

Feel free to tweak:

- **Filename scheme** – edit `prefix = ...` or change `slugify()`  
- **Chunk size / concurrency** – adjust `iter_content(chunk_size=…)` or wrap calls in `concurrent.futures`  
- **Ad-skipping** – post-process with `ffmpeg` silence detection, chapter files, or your preferred AI model.

---
## Roadmap / TODO
- [ ] Optional multithreaded downloads  
- [ ] Support `<podcast:chapters>` tags to auto-skip pre-rolls  
- [ ] CLI flags (`--start-date`, `--end-date`, `--pattern`)  
- [ ] Dockerfile for zero-setup use  

> PRs & issues welcome!

---
## Legal / Fair-Use Notice
Downloading podcast episodes for **personal, time-shifted listening** is generally allowed.  
Redistribution, public re-hosting, or ad-stripping may violate the publisher’s terms.  
Always review the feed’s license and respect creators’ rights.

---
## License
MIT © 2025 mgelsinger 
See `LICENSE` for details.


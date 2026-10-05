"""Refresh the Writing section of index.html from the Substack RSS feeds.

Rewrites only the HTML between <!-- posts:NAME ... --> and <!-- /posts:NAME -->.
If a feed can't be fetched or parsed, that list is left as it is.
Standard library only, so the workflow needs no installs.
"""

import email.utils
import html
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEEDS = ["nabarunwrites", "winninglate"]
SHOWN = 3      # posts visible before "Show more"
TOTAL = 6      # posts listed in all
INDEX = Path(__file__).resolve().parent.parent / "index.html"


def fetch(name):
    req = urllib.request.Request(
        f"https://{name}.substack.com/feed",
        headers={"User-Agent": "Mozilla/5.0 (portfolio feed sync)"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())

    posts = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        date = email.utils.parsedate_to_datetime(item.findtext("pubDate"))
        if title and link.startswith(f"https://{name}.substack.com/"):
            posts.append((date, title, link))
    posts.sort(reverse=True)
    return posts[:TOTAL]


def tidy(title):
    # house style: no em dashes anywhere on the page
    return re.sub(r"\s*—\s*", " · ", title)


def render(posts, indent):
    lines = [f'{indent}<div class="writing-posts">']
    for i, (date, title, link) in enumerate(posts):
        cls = "writing-post" if i < SHOWN else "writing-post is-extra"
        lines += [
            f'{indent}    <a class="{cls}" href="{html.escape(link)}" target="_blank" rel="noopener noreferrer">',
            f'{indent}        <span class="wp-title">{html.escape(tidy(title), quote=False)}</span>',
            f'{indent}        <span class="wp-date">{date.strftime("%b")} {date.day}</span>',
            f"{indent}    </a>",
        ]
    lines.append(f"{indent}</div>")
    extra = len(posts) - SHOWN
    if extra > 0:
        lines += ["", f'{indent}<button type="button" class="writing-morebtn">Show {extra} more ↓</button>']
    return "\n".join(lines)


def main():
    page = INDEX.read_text(encoding="utf-8")
    original = page

    for name in FEEDS:
        block = re.compile(
            rf"(<!-- posts:{name}\b[^>]*-->\n)(.*?)(\n[ \t]*<!-- /posts:{name} -->)", re.S
        )
        m = block.search(page)
        if not m:
            sys.exit(f"markers for {name} not found in index.html")

        try:
            posts = fetch(name)
        except Exception as e:  # network or feed hiccup: keep what's there
            print(f"::warning::{name}: could not read feed ({e}); list left unchanged")
            continue
        if not posts:
            print(f"::warning::{name}: feed had no posts; list left unchanged")
            continue

        indent = re.match(r"[ \t]*", m.group(2)).group(0)
        page = page[: m.start(2)] + render(posts, indent) + page[m.end(2) :]
        print(f"{name}: {', '.join(t for _, t, _ in posts[:SHOWN])}")

    if page != original:
        INDEX.write_text(page, encoding="utf-8")
        print("index.html updated")
    else:
        print("no changes")


if __name__ == "__main__":
    main()

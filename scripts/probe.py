import urllib.request, urllib.parse
F = "https://winninglate.substack.com/feed"
q = urllib.parse.quote(F, safe="")
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}
urls = {
  "direct": F,
  "direct-curl-ua": F,
  "archive-api": "https://winninglate.substack.com/api/v1/archive?sort=new&limit=6",
  "substack.com-profile-api": "https://substack.com/api/v1/archive?sort=new&limit=6",
  "rss2json": f"https://api.rss2json.com/v1/api.json?rss_url={q}",
  "allorigins": f"https://api.allorigins.win/raw?url={q}",
  "codetabs": f"https://api.codetabs.com/v1/proxy?quest={F}",
  "jina": f"https://r.jina.ai/{F}",
  "corsproxy": f"https://corsproxy.io/?url={q}",
  "feedburner-like-feedrapp": f"https://feedrapp.info/?q={q}",
}
for k, u in urls.items():
    h = {"User-Agent": "curl/8.5.0"} if k == "direct-curl-ua" else H
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=25) as r:
            b = r.read()
            ok = b"<item>" in b or b'"items"' in b or b"Two Likes" in b or b"post_date" in b
            print(f"::notice::{k}: {r.status}, {len(b)} bytes, posts found={ok}")
    except Exception as e:
        print(f"::notice::{k}: FAIL {e}")

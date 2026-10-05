import urllib.request, urllib.parse, json
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}
for name in ["winninglate", "nabarunwrites"]:
    q = urllib.parse.quote(f"https://{name}.substack.com/feed", safe="")
    for extra in ["", "&num=6"]:
        u = f"https://feedrapp.info/?q={q}{extra}"
        try:
            b = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=25).read()
            t = b.decode("utf-8", "replace")
            print(f"::notice::{name}{extra} head: {t[:160]!r}")
            try:
                d = json.loads(t); e = d["responseData"]["feed"]["entries"]
                print(f"::notice::{name}{extra} JSON {len(e)} entries; keys {list(e[0])[:8]}; first: {e[0].get('title')} | {e[0].get('publishedDate')} | {e[0].get('link')}")
            except Exception as ex:
                print(f"::notice::{name}{extra} not json: {ex}")
        except Exception as ex:
            print(f"::notice::{name}{extra} FAIL {ex}")

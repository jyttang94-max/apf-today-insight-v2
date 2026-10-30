#!/usr/bin/env python3
"""Build a review-only publication inventory from archived HTML.
HTML files on GitHub are NOT proof that a newsletter was emailed.
Only a separately confirmed sent record may be marked published.
"""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path

class Extract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.href=None
        self.text=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a": self.href=dict(attrs).get("href")
    def handle_data(self,data):
        t=" ".join(data.split())
        if t and self.href and self.href.startswith(("http://","https://")):
            self.links.append({"text":t,"url":self.href})
    def handle_endtag(self,tag):
        if tag=="a": self.href=None

def inventory(paths):
    results=[]
    for path in paths:
        p=Path(path)
        name=p.name
        match=re.search(r"VOL(\\d+)_([0-9]{8})",name,re.I)
        if not match: continue
        parser=Extract()
        parser.feed(p.read_text(encoding="utf-8"))
        links=[]
        seen=set()
        for item in parser.links:
            if item["url"] not in seen:
                links.append(item)
                seen.add(item["url"])
        results.append({"vol":int(match.group(1)),"edition_date":f"{match.group(2)[:4]}-{match.group(2)[4:6]}-{match.group(2)[6:]}",
          "source_file":str(p),"publication_status":"unconfirmed","links":links,
          "note":"Repository HTML presence does not establish delivery or editorial approval"})
    return {"schema_version":"2.0","source":"github_html_inventory","issues":results}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("html",nargs="+")
    p.add_argument("--out",required=True)
    a=p.parse_args()
    data=inventory(a.html)
    Path(a.out).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Inventoried {len(data['issues'])} issue HTML file(s), all publication statuses unconfirmed")
if __name__=="__main__":main()

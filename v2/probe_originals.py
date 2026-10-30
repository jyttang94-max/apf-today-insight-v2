#!/usr/bin/env python3
"""Retrieve original article pages and create auditable evidence for editorial review.
Never mark body_verified automatically: fetching a page is not factual approval.
"""
import argparse
import hashlib
import json
import re
import urllib.request
from datetime import datetime,timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from v2.stage2 import canonical_url

class PageText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip=0
        self.parts=[]
        self.title=[]
        self.in_title=False
    def handle_starttag(self,tag,attrs):
        if tag in ("script","style","nav","footer"): self.skip+=1
        if tag=="title": self.in_title=True
    def handle_endtag(self,tag):
        if tag in ("script","style","nav","footer"): self.skip=max(0,self.skip-1)
        if tag=="title": self.in_title=False
    def handle_data(self,data):
        if self.skip: return
        t=" ".join(data.split())
        if t:
            if self.in_title: self.title.append(t)
            else: self.parts.append(t)

def probe(article,fetcher=None):
    url=canonical_url(article.get("original_url"))
    result={"id":article.get("id"),"candidate_title":article.get("title"),
            "original_url":url or None,"body_verified":False,
            "verification_status":"needs_editor_review"}
    if not url:
        result["verification_status"]="original_url_missing"
        return result
    try:
        if fetcher is None:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; APFEditorialAudit/2.0)"})
            def fetcher(u): return urllib.request.urlopen(req,timeout=12)
        with fetcher(url) as resp:
            final=canonical_url(resp.geturl())
            mime=resp.headers.get("Content-Type","").lower()
            raw=resp.read(2_000_001)
        if len(raw)>2_000_000: raise ValueError("response_too_large")
        if not final or not mime.startswith("text/html"): raise ValueError("non_html_or_invalid_redirect")
        page=PageText()
        page.feed(raw.decode("utf-8",errors="replace"))
        body=" ".join(page.parts)
        result.update({"retrieved_at":datetime.now(timezone.utc).isoformat(),
                       "body_evidence_url":final,"source_title":" ".join(page.title),
                       "body_length":len(body),"body_sha256":hashlib.sha256(body.encode()).hexdigest(),
                       "body_preview":body[:600]})
        result["verification_status"]="retrieved_needs_editor_review" if len(body)>=500 else "insufficient_body"
    except Exception as e:
        result.update({"verification_status":"fetch_failed","error":f"{type(e).__name__}: {str(e)[:180]}"})
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--candidates",required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--limit",type=int,default=20)
    a=p.parse_args()
    if a.limit<1 or a.limit>100: p.error("--limit must be between 1 and 100")
    candidates=json.loads(Path(a.candidates).read_text(encoding="utf-8"))
    rows=[probe(x) for x in candidates["articles"][:a.limit]]
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    Path(a.out).write_text(json.dumps({"edition_date":candidates.get("edition_date"),
       "probed":len(rows),"results":rows},ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"probed":len(rows),"retrieved":sum(x["verification_status"]=="retrieved_needs_editor_review" for x in rows),
       "approved":0},ensure_ascii=False))
if __name__=="__main__":main()

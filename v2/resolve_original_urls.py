#!/usr/bin/env python3
"""Resolve Google News RSS links to publisher URLs where possible.
Fail closed: no inferred publisher URL from headline, no automatic body approval.
"""
import argparse
import json
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit
try:
    from v2.stage2 import canonical_url
except ModuleNotFoundError:
    from stage2 import canonical_url

def resolve(article, opener=None):
    existing=canonical_url(article.get("original_url"))
    if existing:
        return {"id":article.get("id"),"original_url":existing,"status":"existing_unverified"}
    rss=article.get("rss_url")
    if not isinstance(rss,str) or urlsplit(rss).hostname!="news.google.com":
        return {"id":article.get("id"),"original_url":None,"status":"missing_google_news_url"}
    try:
        req=urllib.request.Request(rss,headers={"User-Agent":"Mozilla/5.0"})
        if opener is None: opener=lambda request:urllib.request.urlopen(request,timeout=12)
        with opener(req) as response:
            final=response.geturl()
        canonical=canonical_url(final)
        if canonical:
            return {"id":article.get("id"),"original_url":canonical,"status":"redirect_resolved_unverified"}
        return {"id":article.get("id"),"original_url":None,"status":"unresolved_google_news"}
    except Exception as exc:
        return {"id":article.get("id"),"original_url":None,"status":"request_failed","error":str(exc)[:200]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--candidates",required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--limit",type=int,default=20)
    a=p.parse_args()
    if not 1<=a.limit<=100: p.error("limit must be 1-100")
    payload=json.loads(Path(a.candidates).read_text(encoding="utf-8"))
    results=[resolve(x) for x in payload["articles"][:a.limit]]
    output={"edition_date":payload.get("edition_date"),"results":results,
            "resolved":sum(bool(x["original_url"]) for x in results),
            "unresolved":sum(not x["original_url"] for x in results)}
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    Path(a.out).write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in output.items() if k!="results"},ensure_ascii=False))
if __name__=="__main__":main()

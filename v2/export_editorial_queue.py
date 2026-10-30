#!/usr/bin/env python3
"""Export GitHub candidates for ChatGPT editorial verification without treating URL failure as rejection."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit

def make_queue(payload, resolution=None, limit=40):
    resolution=resolution or {}
    by_id={str(r.get("id")):r for r in resolution.get("results",[]) if isinstance(r,dict)}
    result=[]
    for a in payload.get("articles",[])[:limit]:
        ident=str(a.get("id",""))
        r=by_id.get(ident,{})
        original=r.get("original_url") or a.get("original_url")
        status=r.get("status","not_attempted")
        result.append({
            "candidate_id":ident,"title":a.get("title"),"publisher":a.get("source"),
            "published_at":a.get("published_at"),"category":a.get("category"),
            "discovery_url":a.get("rss_url"),"original_url_hint":original,
            "url_resolution_status":status,
            "editorial_status":"needs_independent_search",
            "search_queries":[
                " ".join(x for x in (a.get("title"),a.get("source")) if x),
                " ".join(x for x in (a.get("title"),) if x)
            ],
            "verification_required":["publisher_or_official_source","article_date","event_identity","core_facts","photo_provenance"],
            "notes":"URL resolution failure is not article rejection. Search independently and record evidence."
        })
    return {"schema_version":"2.0","edition_date":payload.get("edition_date"),
        "phase":payload.get("phase"),"total":len(result),"candidates":result}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--candidates",required=True)
    p.add_argument("--resolution")
    p.add_argument("--out",required=True)
    p.add_argument("--limit",type=int,default=40)
    a=p.parse_args()
    if not 1<=a.limit<=500:p.error("limit must be 1..500")
    payload=json.loads(Path(a.candidates).read_text(encoding="utf-8"))
    resolution=json.loads(Path(a.resolution).read_text(encoding="utf-8")) if a.resolution else None
    data=make_queue(payload,resolution,a.limit)
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"edition_date":data["edition_date"],"queued":data["total"],"rejected_for_url_failure":0},ensure_ascii=False))
if __name__=="__main__":main()

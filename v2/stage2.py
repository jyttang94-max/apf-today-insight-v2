#!/usr/bin/env python3
"""APF V2 stage 2: candidate selection and fail-closed verification/duplicate gate.
Only explicitly verified, evidence-backed articles may become eligible.
Usage: python v2/stage2.py --candidates path --registry v2/publication_registry.json --evidence v2/verified_articles.json --out output.json
"""
import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def canonical_url(value):
    if not isinstance(value,str): return ""
    p=urlsplit(value.strip())
    if p.scheme not in ("http","https") or not p.netloc: return ""
    host=p.netloc.lower().removeprefix("www.")
    if host in ("news.google.com","google.com"): return ""
    query=urlencode([(k,v) for k,v in parse_qsl(p.query) if not k.lower().startswith("utm_") and k not in ("fbclid","gclid")])
    return urlunsplit(("https",host,p.path.rstrip("/") or "/",query,""))

def title_key(value):
    return re.sub(r"[^0-9a-z가-힣]","",str(value).casefold())

def validate_registry(registry):
    if not isinstance(registry,dict) or not isinstance(registry.get("records"),list):
        raise ValueError("registry must be an object with records array")
    for i,r in enumerate(registry["records"]):
        if not isinstance(r,dict) or r.get("status") not in ("published","approved","review"):
            raise ValueError(f"invalid registry record {i}: status")
        if not r.get("title") or not r.get("edition_date"):
            raise ValueError(f"invalid registry record {i}: title/date")
    return registry

def verify_evidence(e):
    if not isinstance(e,dict) or e.get("body_verified") is not True: return False
    if not canonical_url(e.get("original_url")): return False
    if not e.get("verified_at") or not e.get("body_evidence_url"): return False
    if not canonical_url(e["body_evidence_url"]): return False
    if not isinstance(e.get("confirmed_facts"),list) or len(e["confirmed_facts"])<2: return False
    if not all(isinstance(x,str) and x.strip() for x in e["confirmed_facts"]): return False
    if not e.get("event_key") or not e.get("source_title"): return False
    return True

def classify(candidates, registry, evidence):
    validate_registry(registry)
    if not isinstance(candidates,dict) or not isinstance(candidates.get("articles"),list):
        raise ValueError("invalid candidates payload")
    if candidates.get("phase") not in ("morning_merge","evening_collection"):
        raise ValueError("unrecognized phase")
    if not re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}",str(candidates.get("edition_date",""))):
        raise ValueError("missing edition_date")
    if not isinstance(evidence,dict): raise ValueError("evidence must be object keyed by candidate ID")
    prior=[r for r in registry["records"] if r["status"] in ("published","approved")]
    known_urls={canonical_url(r.get("original_url")) for r in prior}
    known_titles={title_key(r["title"]) for r in prior}
    known_events={r.get("event_key") for r in prior if r.get("event_key")}
    result=[]; eligible_events=set(); eligible_urls=set()
    for a in candidates["articles"]:
        ident=str(a.get("id",""))
        e=evidence.get(ident,{})
        reason=[]
        if not verify_evidence(e): reason.append("BODY_NOT_VERIFIED")
        if a.get("body_verified") is not True and not verify_evidence(e): reason.append("COLLECTOR_UNVERIFIED")
        url=canonical_url(e.get("original_url"))
        if url and url in known_urls: reason.append("PRIOR_URL")
        if title_key(a.get("title","")) in known_titles: reason.append("PRIOR_TITLE")
        event=e.get("event_key")
        if event and event in known_events: reason.append("PRIOR_EVENT")
        if event and event in eligible_events: reason.append("SAME_BATCH_EVENT")
        if url and url in eligible_urls: reason.append("SAME_BATCH_URL")
        if not registry.get("coverage_complete",False): reason.append("HISTORY_INCOMPLETE")
        if not reason:
            eligible_events.add(event); eligible_urls.add(url)
        result.append({"id":ident,"title":a.get("title"),"original_url":url or None,
            "event_key":event,"status":"eligible" if not reason else "hold","reasons":reason})
    return {"edition_date":candidates["edition_date"],"phase":candidates["phase"],
        "registry_coverage_complete":registry.get("coverage_complete",False),
        "total":len(result),"eligible":sum(x["status"]=="eligible" for x in result),
        "held":sum(x["status"]=="hold" for x in result),"results":result}

def main():
    p=argparse.ArgumentParser()
    for name in ("candidates","registry","evidence","out"): p.add_argument("--"+name,required=True)
    a=p.parse_args()
    output=classify(load(a.candidates),load(a.registry),load(a.evidence))
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    Path(a.out).write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in output.items() if k!="results"},ensure_ascii=False))
if __name__=="__main__": main()

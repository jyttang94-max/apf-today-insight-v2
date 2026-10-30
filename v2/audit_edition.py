#!/usr/bin/env python3
"""Fail-closed editorial QA; stdlib only. Usage: python v2/audit_edition.py edition.json"""
import json, sys, re, hashlib
from pathlib import Path
from urllib.parse import urlparse
def check(data):
    errors=[]
    required=("vol","edition_date","master_sha256","articles","book","insight","status")
    for key in required:
        if key not in data: errors.append("missing:"+key)
    slots=set(); events=set(); urls=set()
    for i,a in enumerate(data.get("articles",[])):
        slot=a.get("slot","")
        if slot in slots: errors.append(f"duplicate slot:{slot}")
        slots.add(slot)
        if not a.get("body_verified"): errors.append(f"{slot}:body not verified")
        u=a.get("original_url","")
        if urlparse(u).scheme!="https" or "news.google.com" in u: errors.append(f"{slot}:not original URL")
        if u in urls: errors.append(f"{slot}:duplicate URL")
        urls.add(u)
        event=a.get("event_key","")
        if not event: errors.append(f"{slot}:missing event key")
        if event in events: errors.append(f"{slot}:duplicate event")
        events.add(event)
        if not a.get("verified_facts"): errors.append(f"{slot}:no confirmed facts")
        im=a.get("image") or {}
        if slot not in ("women","beauty"):
            if not im.get("verified") or not im.get("embedded"): errors.append(f"{slot}:image not verified/embedded")
            if not re.fullmatch("[a-f0-9]{64}",im.get("sha256","")): errors.append(f"{slot}:image SHA missing")
    for slot in ("women","beauty","academic","culture","youth","editor"):
        if slot not in slots: errors.append("missing slot:"+slot)
    b=data.get("book") or {}
    if not b.get("cover_verified") or not re.fullmatch("[a-f0-9]{64}",b.get("cover_sha256","")):
        errors.append("book:official cover not verified")
    if not b.get("official_url","").startswith("https://"): errors.append("book:official URL missing")
    if len(data.get("insight",""))<30: errors.append("insight too short")
    return errors
if __name__=="__main__":
    if len(sys.argv)!=2: sys.exit("usage: python v2/audit_edition.py edition.json")
    data=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors=check(data)
    print(json.dumps({"passed":not errors,"errors":errors},ensure_ascii=False,indent=2))
    sys.exit(1 if errors else 0)

#!/usr/bin/env python3
"""Prepare a non-publishing editorial report from verified evidence and provisional history."""
import argparse,json
from pathlib import Path
try:
 from v2.stage2 import verify_evidence,canonical_url,title_key
except ModuleNotFoundError:
 from stage2 import verify_evidence,canonical_url,title_key

def review(candidates,evidence,history):
 prior_urls={canonical_url(x.get("url")) for x in history.get("records",[])}
 prior_titles={title_key(x.get("title_hint")) for x in history.get("records",[])}
 rows=[]
 for a in candidates.get("articles",[]):
  key=str(a.get("id",""));ev=evidence.get(key,{})
  verified=verify_evidence(ev)
  url=canonical_url(ev.get("original_url"))
  possible=bool(url and url in prior_urls or title_key(a.get("title","")) in prior_titles)
  rows.append({"id":key,"title":a.get("title"),"publisher":a.get("source"),
   "source_verified":verified,"potential_history_duplicate":possible,
   "editorial_status":"review_candidate" if verified and not possible else "hold",
   "reasons":([] if verified else ["SOURCE_EVIDENCE_MISSING"])+(["POTENTIAL_HISTORY_DUPLICATE"] if possible else []),
   "image_status":"not_checked","note":"No final approval; incomplete history must be reconciled"})
 return {"edition_date":candidates.get("edition_date"),"history_complete":False,
  "total":len(rows),"review_candidates":sum(x["editorial_status"]=="review_candidate" for x in rows),
  "items":rows,"publication_approved":False}

def main():
 p=argparse.ArgumentParser()
 for k in ("candidates","evidence","history","out"):p.add_argument("--"+k,required=True)
 a=p.parse_args();load=lambda f:json.loads(Path(f).read_text(encoding="utf-8"))
 d=review(load(a.candidates),load(a.evidence),load(a.history))
 out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"total":d["total"],"review_candidates":d["review_candidates"],"publication_approved":False}))
if __name__=="__main__":main()

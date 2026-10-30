#!/usr/bin/env python3
"""Export balanced editorial queues from ALL APF collector categories.
Collection category is a hint only: no candidate is marked verified.
"""
import argparse,json,re
from pathlib import Path
CATEGORIES=("인재육성·학술연구","문화예술","청년지원","여성의 삶","아름다움의 의미")
def norm(t):return re.sub(r"[^가-힣a-z0-9]","",str(t).lower())
def balanced(payload,per_category=20):
 result={k:[] for k in CATEGORIES};seen=set()
 for a in payload.get("articles",[]):
  cat=a.get("category")
  if cat not in result:continue
  key=norm(a.get("title",""))
  if not key or key in seen:continue
  seen.add(key)
  if len(result[cat])>=per_category:continue
  result[cat].append({"candidate_id":a.get("id"),"collector_category":cat,"title":a.get("title"),
   "publisher":a.get("source"),"published_at":a.get("published_at"),
   "rss_url":a.get("rss_url"),"original_url_hint":a.get("original_url"),
   "verification_status":"unverified","category_status":"requires_editorial_review",
   "search_queries":[f"{a.get('title','')} {a.get('source','')}",str(a.get("title",""))]})
 return {"edition_date":payload.get("edition_date"),"collector_generated_at":payload.get("generated_at"),
  "total_collected":len(payload.get("articles",[])),"category_counts":{k:sum(a.get("category")==k for a in payload.get("articles",[])) for k in CATEGORIES},
  "queues":result,"note":"No original article bodies have been verified by this export. Human/editorial reclassification required."}
def main():
 p=argparse.ArgumentParser();p.add_argument("--candidates",required=True);p.add_argument("--out",required=True);p.add_argument("--per-category",type=int,default=20)
 a=p.parse_args();d=balanced(json.loads(Path(a.candidates).read_text(encoding="utf-8")),a.per_category)
 o=Path(a.out);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"counts":d["category_counts"],"exported":{k:len(v) for k,v in d["queues"].items()}},ensure_ascii=False))
if __name__=="__main__":main()

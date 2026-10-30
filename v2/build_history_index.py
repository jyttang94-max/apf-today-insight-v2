#!/usr/bin/env python3
"""Build provisional issue-link index without claiming delivery or approval."""
import argparse,json,re
from pathlib import Path
from urllib.parse import urlsplit
try:
 from v2.inventory_issues import inventory
except ModuleNotFoundError:
 from inventory_issues import inventory

def index_issues(paths):
 issues=inventory(paths)["issues"]
 rows=[]
 for issue in issues:
  for link in issue["links"]:
   url=link["url"]
   host=urlsplit(url).hostname or ""
   if not host or host in ("instagram.com","www.instagram.com","youtube.com","www.youtube.com","www.amorepacificfoundation.org"):continue
   title=" ".join(link["text"].split())
   if not title or len(title)<8:continue
   rows.append({"vol":issue["vol"],"edition_date":issue["edition_date"],"title_hint":title,"url":url,
    "status":"unconfirmed_issue_link","source_file":issue["source_file"]})
 return {"schema_version":"2.0","coverage_complete":False,"issues_found":len(issues),
  "records":rows,"note":"Links extracted from HTML are not proof of sent, approved, or even editorial article status. Manually reconcile before promotion."}

def main():
 p=argparse.ArgumentParser();p.add_argument("html",nargs="+");p.add_argument("--out",required=True);a=p.parse_args()
 result=index_issues(a.html)
 out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"issues_found":result["issues_found"],"link_hints":len(result["records"]),"coverage_complete":False}))
if __name__=="__main__":main()

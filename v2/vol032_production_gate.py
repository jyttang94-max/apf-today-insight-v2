#!/usr/bin/env python3
"""Guard VOL.032 content replacement. Never emit relabelled stale MASTER as a new edition."""
import argparse,json,re
from pathlib import Path
from urllib.parse import urlsplit

REQUIRED=("women","beauty","academic","arts","youth")
def preflight(package):
 stories=package.get("stories",[])
 slots={s.get("slot") for s in stories}
 errors=[]
 for slot in REQUIRED:
  if slot not in slots: errors.append("MISSING_SLOT:"+slot)
 for s in stories:
  u=urlsplit(s.get("original_url",""))
  if s.get("body_verified") is not True or u.scheme!="https" or not u.netloc or not s.get("body"):
   errors.append("UNVERIFIED:"+str(s.get("slot")))
  if s.get("image_status")!="embedded_verified" and s.get("slot") in ("academic","arts","youth"):
   errors.append("IMAGE_NOT_READY:"+str(s.get("slot")))
 if not package.get("prior_history_reconciled",False):errors.append("HISTORY_NOT_RECONCILED")
 if not package.get("book_verified",False):errors.append("BOOK_NOT_VERIFIED")
 if not package.get("editors_pick_verified",False):errors.append("EDITORS_PICK_NOT_VERIFIED")
 return {"ready_for_full_html":not errors,"errors":errors,"verified_stories":sum(s.get("body_verified") is True for s in stories)}
def main():
 p=argparse.ArgumentParser();p.add_argument("--editorial",required=True);p.add_argument("--out",required=True)
 a=p.parse_args();d=json.loads(Path(a.editorial).read_text(encoding="utf-8"));result=preflight(d)
 out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps(result,ensure_ascii=False))
 if result["errors"]:print("No HTML emitted: VOL.032 content replacement requires verified complete slots.")
if __name__=="__main__":main()

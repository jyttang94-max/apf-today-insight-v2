#!/usr/bin/env python3
"""Select latest collector run by generated_at, not stale data/latest.json."""
import argparse,json
from pathlib import Path
def select(root,cutoff=None):
 rows=[]
 for p in Path(root).glob("*/candidates.json"):
  try:
   d=json.loads(p.read_text(encoding="utf-8"))
   ts=d.get("generated_at","")
   if ts and (not cutoff or ts<=cutoff):
    rows.append((ts,p))
  except (OSError,ValueError):continue
 if not rows:raise RuntimeError("No eligible collector run found")
 return str(max(rows,key=lambda x:x[0])[1])
def main():
 p=argparse.ArgumentParser();p.add_argument("--root",default="data/v5/runs");p.add_argument("--cutoff");a=p.parse_args()
 print(select(a.root,a.cutoff))
if __name__=="__main__":main()

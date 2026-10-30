#!/usr/bin/env python3
"""Produce a standalone editorial proof, never a VOL.032 final or approved sendable HTML.
The approved VOL.032 master is not copied until all publication gates pass.
"""
import argparse,html,json
from pathlib import Path
ORDER=(("women","여성의 삶"),("beauty","아름다움의 의미"),("academic","인재육성 및 학술연구"),("arts","문화예술"),("youth","청년지원"))
def render(data):
 stories={s["slot"]:s for s in data.get("stories",[])}
 blocks=[]
 for key,label in ORDER:
  s=stories.get(key)
  if not s:blocks.append(f'<section><h2>{label}</h2><p>기사 검증 대기</p></section>');continue
  title=html.escape(s["title"]);lead=html.escape(s["lead"]);body=html.escape(s["body"])
  url=html.escape(s["original_url"],quote=True)
  blocks.append(f'<section><h2>{label}</h2><h3>{title}</h3><p class="lead">{lead}</p><p>{body}</p><p><a href="{url}">원문 확인</a> | 사진: {html.escape(s.get("image_status","unknown"))}</p></section>')
 ins=data.get("insight",{})
 blocks.append('<section><h2>FROM NEWS TO INSIGHT</h2><h3>'+html.escape(ins.get("title","검증 대기"))+'</h3><p>'+html.escape(ins.get("body",""))+'</p><p>'+html.escape(ins.get("question",""))+'</p></section>')
 blocks.append('<section><h2>EDITOR’S PICKS</h2><p>별도 원문 검증 대기</p></section>')
 blocks.append('<section><h2>美리보기</h2><p>도서 및 표지 검증 대기</p></section>')
 return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>APF TODAY INSIGHT | EDITORIAL PROOF ONLY</title><style>body{background:#f3f5f7;font-family:Arial,sans-serif;color:#193648}main{max-width:680px;margin:24px auto;background:white;padding:28px;box-sizing:border-box}header{background:#17384e;color:white;padding:24px}section{padding:22px 0;border-bottom:1px solid #dce4e9}h2{font-size:15px}h3{font-size:20px}.lead{font-weight:bold;color:#536b79}p{font-size:14px;line-height:1.9}.warning{color:#8b3800;font-weight:bold}</style></head><body><main><header><h1>APF TODAY INSIGHT</h1><p>EDITORIAL PROOF / NOT FOR SENDING</p></header><p class="warning">콘텐츠 검토용 별도 미리보기입니다. VOL.032 승인 디자인을 재현한 최종 HTML이 아닙니다. 기발행 이력, 원본 사진, 책, EDITOR’S PICKS 검증 전 발송 금지.</p>'+''.join(blocks)+'</main></body></html>'
def main():
 p=argparse.ArgumentParser();p.add_argument("--editorial",required=True);p.add_argument("--out",required=True);a=p.parse_args()
 data=json.loads(Path(a.editorial).read_text(encoding="utf-8"));o=Path(a.out);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(render(data),encoding="utf-8")
 print("Editorial proof written:",o,"verified story slots:",len(data.get("stories",[])))
if __name__=="__main__":main()

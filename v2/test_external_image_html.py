#!/usr/bin/env python3
"""Network-to-HTML photo test. NEVER use generated HTML for publication."""
import argparse,base64,hashlib,io,json,re,urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from PIL import Image,ImageOps

class Metadata(HTMLParser):
 def __init__(self): super().__init__();self.images=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=="meta" and a.get("property") in ("og:image","og:image:url") and a.get("content"): self.images.append(a["content"])

def get(url):
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; APF-Image-Verification/1.0)","Accept":"image/avif,image/webp,image/*,text/html;q=0.8,*/*;q=0.5"})
 with urllib.request.urlopen(req,timeout=25) as r: return r.read(12_000_000),r.headers.get("Content-Type","")
def main():
 p=argparse.ArgumentParser();p.add_argument("--article-url",required=True);p.add_argument("--html",required=True);p.add_argument("--out",required=True);p.add_argument("--report",required=True);a=p.parse_args()
 raw,ctype=get(a.article_url);assert "html" in ctype.lower(),"article page is not HTML"
 parser=Metadata();parser.feed(raw.decode("utf-8","replace"))
 if not parser.images: raise RuntimeError("No og:image found; do not substitute another photo")
 photo_url=urljoin(a.article_url,parser.images[0]);photo,mime=get(photo_url)
 if not mime.lower().startswith("image/"):raise RuntimeError("Image URL did not return image content")
 with Image.open(io.BytesIO(photo)) as img:
  img.load()
  if img.width<278 or img.height<150:raise RuntimeError("Source image too small")
  output=ImageOps.fit(img.convert("RGB"),(278,150),method=Image.Resampling.LANCZOS)
  buff=io.BytesIO();output.save(buff,format="JPEG",quality=88)
 jpeg=buff.getvalue()
 html=Path(a.html).read_text(encoding="utf-8")
 m=re.search(r'(<img\b[^>]*?\bsrc=")(data:image/jpeg;base64,[^"]+)(")',html,re.I|re.S)
 if not m:raise RuntimeError("No existing embedded JPEG image slot found")
 data_uri="data:image/jpeg;base64,"+base64.b64encode(jpeg).decode("ascii")
 html=html[:m.start(2)]+data_uri+html[m.end(2):]
 notice='<div style="padding:15px;background:#fff0c2;color:#603700;font-weight:bold;text-align:center">EXTERNAL IMAGE DOWNLOAD TEST — NOT FOR PUBLICATION. First image replaced from external article. Other article text unchanged.</div>'
 html=re.sub(r'(<body[^>]*>)',lambda z:z.group(1)+notice,html,count=1,flags=re.I)
 out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(html,encoding="utf-8")
 check=re.search(r'<img\b[^>]*?\bsrc="(data:image/jpeg;base64,[^"]+)"',out.read_text(encoding="utf-8"),re.I|re.S)
 assert check and base64.b64decode(check.group(1).split(",",1)[1])==jpeg
 assert Image.open(io.BytesIO(jpeg)).size==(278,150)
 report={"result":"PASS","article_url":a.article_url,"image_url":photo_url,"downloaded_bytes":len(photo),"source_sha256":hashlib.sha256(photo).hexdigest(),"jpeg_sha256":hashlib.sha256(jpeg).hexdigest(),"output_pixels":[278,150],"html":str(out),"notice":"Visual appearance and image/article correspondence require editorial review; do not publish"}
 Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__":main()

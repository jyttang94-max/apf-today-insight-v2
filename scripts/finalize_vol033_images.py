from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageOps
import base64,io,requests,json,re,hashlib
src=Path("dist/APF_TODAY_INSIGHT_VOL033_20261030_EDITORIAL_IMAGE_REVIEW.html")
s=BeautifulSoup(src.read_text(encoding="utf-8"),"html.parser")
imgs=s.find_all("img")
assert len(imgs)==5,f"Expected 5 images, found {len(imgs)}"
sources={
0:("https://www.otoki.com/pds/editor/2610/6243e43e3dc54fb3a82e923b31708249.jpg","오뚜기함태호재단 제35회 학술상 시상식 / 오뚜기 제공",(278,150)),
3:("https://img.asiatoday.co.kr/file/2026y/10m/27d/20261027000732383_1793054377_1.jpg","2026 제21회 인문주간 기념 세미나 / 한국인문사회총연합회 제공",(230,189))
}
provenance={}
for idx,(url,alt,size) in sources.items():
 r=requests.get(url,timeout=30,headers={"User-Agent":"Mozilla/5.0"})
 r.raise_for_status()
 im=Image.open(io.BytesIO(r.content)).convert("RGB")
 assert im.width>=size[0] and im.height>=size[1],(idx,im.size)
 im=ImageOps.fit(im,size,method=Image.Resampling.LANCZOS,centering=(.5,.45))
 out=io.BytesIO();im.save(out,"JPEG",quality=85,optimize=True)
 imgs[idx]["src"]="data:image/jpeg;base64,"+base64.b64encode(out.getvalue()).decode()
 imgs[idx]["alt"]=alt
 provenance[str(idx)]={"url":url,"size":list(size),"sha256":hashlib.sha256(out.getvalue()).hexdigest()}
for i,im in enumerate(imgs):
 v=im.get("src","")
 assert v.startswith("data:image/jpeg;base64,"),(i,v[:100])
 data=base64.b64decode(v.split(",",1)[1],validate=True)
 obj=Image.open(io.BytesIO(data));obj.verify()
 provenance.setdefault(str(i),{})["sha256"]=hashlib.sha256(data).hexdigest()
 provenance[str(i)]["bytes"]=len(data)
# The selected editor photo must link to its own source, never the culture story.
a=imgs[3].find_parent("a")
assert a and "asiatoday" in a.get("href",""),a
# Image captions must not carry previous-edition photo credits.
text=s.get_text(" ",strip=True)
for stale in ["VOL. 032","CJ문화재단","국립부경대","청년재단","벤자맹 주아노","니콜 네리그","박서보와 흐엉"]:
 assert stale not in text,stale
for a in s.find_all("a",href=True):
 assert "google.com/search" not in a["href"],a["href"]
out=Path("dist/APF_TODAY_INSIGHT_VOL033_20261030_FINAL.html")
out.write_text(str(s),encoding="utf-8")
Path("dist/APF_VOL033_IMAGE_AUDIT.json").write_text(json.dumps(provenance,ensure_ascii=False,indent=2),encoding="utf-8")
print("FINAL CREATED",out,out.stat().st_size,"embedded images",len(imgs))
print("IMAGE PROVENANCE",json.dumps(provenance,ensure_ascii=False))

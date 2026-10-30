import base64, io, json, re, time
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps
S = requests.Session()
S.headers.update({"User-Agent":"Mozilla/5.0 (compatible; APFNewsletter/1.0)"})
MASTER=Path("assets/master-current.html")
s=BeautifulSoup(MASTER.read_text(encoding="utf-8"),"html.parser")
sources=[
("https://www.otoki.com/pr/news-detail?idx=1067",["오뚜기","함태호"],(278,150)),
("https://www.yna.co.kr/amp/view/AKR20261029179600005",["서울문화재단","커넥트"],(278,150)),
("https://www.kmib.co.kr/",["자립준비청년","AI"],(278,150)),
("https://www.yna.co.kr/amp/view/AKR20261029179600005",["서울문화재단","커넥트"],(230,189)),
("https://www.yes24.com/product/goods/13866370",["동아시아","표지"],(118,157))]
fallbacks=[
["https://www.dailyenews.co.kr/news/articleView.html?idxno=54166","https://www.cnbnews.com/news/articleView.html?idxno=1021540"],
["https://www.sfac.or.kr/"],
[],
["https://www.sfac.or.kr/"],
["https://image.yes24.com/goods/13866370/XL"]]
def get(url):
 r=S.get(url,timeout=25);r.raise_for_status();return r
def candidates(url):
 if re.search(r"\.(?:jpe?g|png|webp)(?:\?|$)",url,re.I) or "image.yes24.com" in url:
  return [url]
 try:
  page=get(url); html=BeautifulSoup(page.content,"html.parser")
 except Exception as e:
  print("PAGE ERROR",url,str(e));return []
 urls=[]
 for tag in html.find_all("meta"):
  if tag.get("property") in ["og:image","og:image:url","twitter:image"] or tag.get("name")=="twitter:image":
   if tag.get("content"):urls.append(urljoin(page.url,tag["content"]))
 for im in html.find_all("img"):
  for key in ["data-src","data-original","src","srcset"]:
   v=im.get(key)
   if v:urls.append(urljoin(page.url,v.split(" ")[0]))
 return list(dict.fromkeys(x for x in urls if x.startswith("http")))
def photo(urls,size):
 for url in urls:
  try:
   r=get(url)
   if len(r.content)<3000:continue
   img=Image.open(io.BytesIO(r.content)).convert("RGB")
   if img.width<120 or img.height<100:continue
   if size==(118,157): img=ImageOps.pad(img,size,color="white",method=Image.Resampling.LANCZOS)
   else: img=ImageOps.fit(img,size,method=Image.Resampling.LANCZOS)
   b=io.BytesIO();img.save(b,format="JPEG",quality=86,optimize=True)
   return "data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode(),url
  except Exception as e: print("IMAGE ERROR",url,str(e)[:150])
 return None,None
imgs=s.find_all("img")
assert len(imgs)==5
results=[]
for i,((src,keywords,size),alternatives) in enumerate(zip(sources,fallbacks)):
 urls=[]
 for page in [src]+alternatives:
  urls+=candidates(page)
 data,used=photo(list(dict.fromkeys(urls)),size)
 if not data:raise RuntimeError(f"Missing verified image {i}: {src}")
 imgs[i]["src"]=data;imgs[i]["width"]=str(size[0]);imgs[i]["height"]=str(size[1])
 imgs[i]["alt"]=["오뚜기함태호재단 제35회 학술상 수상 기념사진","서울 커넥트 스테이지 행사 사진","자립준비청년 지원 관련 기사 사진","서울 커넥트 스테이지 행사 사진","동아시아 전통 인테리어 장식과 미 도서 표지"][i]
 results.append({"slot":i,"source":used,"bytes":len(data)})
 print("SUCCESS",i,used)
# Update editorial copy using safe, limited replacements. Preserve all original image tables.
replacements={
"VOL.032":"VOL.033","2026.10.29":"2026.10.30",
"국립부경대, 4개국 연구자와 해양인문학 협력 논의":"오뚜기함태호재단, 제35회 학술상 시상",
"CJ문화재단, 지원 음악인과 청소년 잇는 재즈위크":"서울문화재단, 예비 예술가 22개 팀 선정",
"『논어는 아름답다』":"『동아시아 전통 인테리어 장식과 미』",
}
for node in list(s.find_all(string=True)):
 old=str(node);new=old
 for a,b in replacements.items():new=new.replace(a,b)
 if new!=old:node.replace_with(new)
for a in s.find_all("a",href=True):
 if "viva100.com" in a["href"]:a["href"]=sources[0][0]
 elif "newspim.com" in a["href"]:a["href"]=sources[1][0]
 elif "lawleader.co.kr" in a["href"]:a["href"]=sources[2][0]
 elif "ascf.amorepacific.co.kr/publishedView.do?seq=115" in a["href"]:a["href"]=sources[4][0]
out=Path("dist/APF_TODAY_INSIGHT_VOL033_20261030_IMAGE_BUILD.html")
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(str(s),encoding="utf-8")
Path("dist/vol033-image-provenance.json").write_text(json.dumps(results,ensure_ascii=False,indent=2))
assert len(BeautifulSoup(out.read_text(),"html.parser").find_all("img"))==5
print("DONE",out,out.stat().st_size)

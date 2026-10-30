import requests
from bs4 import BeautifulSoup
from PIL import Image,ImageOps
from io import BytesIO
import base64,re,json
from pathlib import Path
S=requests.Session();S.headers.update({"User-Agent":"Mozilla/5.0"})
def images(url):
 r=S.get(url,timeout=20);r.raise_for_status()
 soup=BeautifulSoup(r.content,"html.parser")
 arr=[]
 for im in soup.select("img"):
  src=im.get("data-src") or im.get("src") or ""
  if not src.startswith("http"):src=requests.compat.urljoin(r.url,src)
  if src.startswith("http"):arr.append((src,im.get("alt",""),im.get("class","")))
 return arr
for label,url in [
 ("otoki","https://www.otoki.com/pr/news-detail?idx=1067"),
 ("editor","https://ww2.asiatoday.co.kr/kn/view.php?key=20261027000732383")]:
 try:
  arr=images(url)
  print("CANDIDATES",label,json.dumps(arr[:30],ensure_ascii=False)[:7000])
 except Exception as e:print("ERROR",label,repr(e))
for url in ["https://www.kmib.co.kr/article/view.asp?arcid=20261029500899","https://www.kmib.co.kr/article/view.asp?arcid=00291029500899","https://www.kmib.co.kr/article/view.asp?arcid=20261029500899&code=11131100"]:
 try:
  r=S.get(url,timeout=15)
  print("KMIB",r.status_code,r.url,r.text[:200].replace("\n"," "))
 except Exception as e:print("KMIB ERR",str(e)[:160])

from urllib.parse import quote
for engine,url in [
 ("bing","https://www.bing.com/search?q="+quote('"중소기업에 AI 기술 전수" "자립준비청년에 희망 사다리"')),
 ("naver","https://search.naver.com/search.naver?where=news&query="+quote('중소기업에 AI 기술 전수 자립준비청년에 희망 사다리')),
 ("google","https://www.google.com/search?q="+quote('"중소기업에 AI 기술 전수" "자립준비청년"'))]:
 try:
  r=S.get(url,timeout=20);sp=BeautifulSoup(r.text,"html.parser")
  links=[(a.get_text(" ",strip=True)[:80],a.get("href","")) for a in sp.select("a[href]") if "kmib" in a.get("href","") or "news.naver.com" in a.get("href","")]
  print("SEARCH",engine,r.status_code,json.dumps(links[:15],ensure_ascii=False)[:6000])
 except Exception as e:print("SEARCH ERR",engine,repr(e))
try:
 r=S.get("https://ww2.asiatoday.co.kr/kn/view.php?key=20261027000732383",timeout=20)
 sp=BeautifulSoup(r.text,"html.parser")
 print("EDITOR META",[(m.get("property"),m.get("content")) for m in sp.select("meta[property]") if "image" in (m.get("property") or "")][:5])
 print("EDITOR ARTICLE IMG",[(im.get("src"),im.get("data-src"),im.get("alt")) for im in sp.select("div.article img, div.view img, figure img, .news_view img")][:10])
except Exception as e:print("EDITOR META ERR",repr(e))

import xml.etree.ElementTree as ET
rss="https://news.google.com/rss/search?q="+quote('"중소기업에 AI 기술 전수" "자립준비청년"')+"&hl=ko&gl=KR&ceid=KR:ko"
try:
 r=S.get(rss,timeout=20);root=ET.fromstring(r.content)
 for item in root.findall(".//item")[:8]:
  print("GOOGLE NEWS",item.findtext("title"),item.findtext("link"))
except Exception as e:print("GOOGLE NEWS ERR",repr(e))

u="https://news.google.com/rss/articles/CBMiWEFVX3lxTE5ydXRySGJxZFBFVlZpb1NZSmlWN3d6NW51ckd5N2t2MDJrT0FydUNNd1hzNGJEMG5IcnAwVEJjczJqRWFHMFhXWWNXWFRTdWRoT0g2M2JmOUI?oc=5"
try:
 r=S.get(u,timeout=20,allow_redirects=True)
 print("GOOGLE REDIRECT",r.status_code,r.url,"kmib" in r.text.lower(),r.text[:140].replace("\n"," "))
except Exception as e:print("GOOGLE REDIRECT ERR",repr(e))

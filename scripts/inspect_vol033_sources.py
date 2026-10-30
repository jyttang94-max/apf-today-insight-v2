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

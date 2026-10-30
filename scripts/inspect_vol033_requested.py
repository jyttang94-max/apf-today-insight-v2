import requests
from bs4 import BeautifulSoup
import json,re
s=requests.Session();s.headers.update({"User-Agent":"Mozilla/5.0"})
urls=["https://www.news1.kr/industry/general-industry/6334458","https://www.amorepacificfoundation.org","https://www.kmib.co.kr/"]
for u in urls:
 try:
  r=s.get(u,timeout=20)
  soup=BeautifulSoup(r.content,"html.parser")
  print("PAGE",u,"STATUS",r.status_code,"TITLE",soup.title.get_text(" ",strip=True) if soup.title else "NONE")
  print("META",[(x.get("property") or x.get("name"),x.get("content")) for x in soup.find_all("meta") if (x.get("property") or x.get("name")) in ["og:title","og:image","description","og:description","article:published_time"]][:10])
  print("TEXT",soup.get_text(" ",strip=True)[:3500])
  print("IMG",[(x.get("src"),x.get("data-src"),x.get("alt")) for x in soup.select("article img, .article img, .news_view img")][:10])
 except Exception as e:print("ERR",u,repr(e))

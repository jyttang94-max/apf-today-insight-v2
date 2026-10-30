from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from bs4 import BeautifulSoup
import base64,io,json,hashlib
from PIL import Image
html=Path("dist/APF_TODAY_INSIGHT_VOL033_20261030_FINAL.html")
s=BeautifulSoup(html.read_text(encoding="utf-8"),"html.parser")
imgs=s.find_all("img")
assert len(imgs)==5
for i,img in enumerate(imgs):
 src=img.get("src","")
 assert src.startswith("data:image/jpeg;base64,"),(i,src[:100])
 data=base64.b64decode(src.split(",",1)[1],validate=True)
 im=Image.open(io.BytesIO(data));im.verify()
 assert im.format=="JPEG"
for old in ["VOL. 032","니콜 네리그","박서보와 흐엉","CJ문화재단","청년재단","벤자맹 주아노","국립부경대"]:
 assert old not in s.get_text(" ",strip=True),old
assert not any(a.get("href")=="https://www.kmib.co.kr/" for a in s.find_all("a",href=True))
out=Path("dist/APF_TODAY_INSIGHT_VOL033_20261030_FINAL.zip")
with ZipFile(out,"w",compression=ZIP_DEFLATED,compresslevel=9) as z:
 z.write(html,arcname=html.name)
 z.write("dist/APF_VOL033_IMAGE_AUDIT.json",arcname="APF_VOL033_IMAGE_AUDIT.json")
print("ZIP VERIFIED",out,out.stat().st_size,"images",len(imgs))

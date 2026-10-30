from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import io,base64,json
s=BeautifulSoup(Path("dist/APF_TODAY_INSIGHT_VOL033_20261030_FINAL.html").read_text(encoding="utf-8"),"html.parser")
data={}
for i,img in enumerate(s.find_all("img")):
 if i==0:continue
 raw=base64.b64decode(img["src"].split(",",1)[1])
 im=Image.open(io.BytesIO(raw)).convert("RGB")
 out=io.BytesIO();im.save(out,format="JPEG",quality=47,optimize=True)
 data[str(i)]=base64.b64encode(out.getvalue()).decode()
Path("dist/vol033_packed_images.json").write_text(json.dumps(data,separators=(",",":")))
print("Packed image bytes:",[(i,len(v)) for i,v in data.items()])

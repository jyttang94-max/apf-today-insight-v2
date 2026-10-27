#!/usr/bin/env python3
"""Collect source-page images for editorial review. Never fabricates placeholders."""
import argparse
import hashlib
import io
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

SOURCES = [
    ("women_kwdi", "한국여성정책연구원 성평등 정책", "https://www.kwdi.re.kr/plaza/bodoView.do?idx=134397&p=1"),
    ("beauty_sema", "서울시립미술관 린 허쉬만 리슨", "https://sema.seoul.go.kr/kr/whatson/exhibition/detail?exNo=1559068"),
    ("research_humanities", "제21회 인문주간", "https://www.moe.go.kr/boardCnts/viewRenew.do?boardID=294&boardSeq=107483&lev=0&m=020402&opType=N&page=1&s=moe&searchType=null&statusYN=W"),
    ("culture_cheonan", "천안시립미술관 접근성 세미나", "https://www.asanfocus.co.kr/news/articleView.html?idxno=52795"),
    ("youth_woojin", "우진문화재단 청년미술상", "https://www.yna.co.kr/amp/view/AKR20261026128500055"),
    ("pick_hansik", "첫 한식의 날", "https://m.korea.kr/briefing/pressReleaseView.do?newsId=156786303"),
    ("book_beautiful_person", "아시아의 美 아름다운 사람 표지", "https://www.apgroup.com/int/ko/misc/news/2018-03-30.html"),
]
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; APF-EditorialImageReview/1.0)"}
def candidates(html, base):
    soup = BeautifulSoup(html, "html.parser")
    found = []
    for m in soup.select('meta[property="og:image"],meta[name="twitter:image"],meta[property="twitter:image"]'):
        found.append((m.get("content"), "metadata"))
    for img in soup.select("article img, main img, .article img, .view_cont img, .content img, img"):
        for attr in ("data-src", "data-original", "data-lazy-src", "src"):
            if img.get(attr):
                found.append((img[attr], "page_image"))
                break
    for source in soup.select("source[srcset],img[srcset]"):
        found.append((source["srcset"].split(",")[0].strip().split(" ")[0], "srcset"))
    seen = set()
    for raw, origin in found:
        if not raw or raw.startswith(("data:", "blob:", "javascript:")):
            continue
        url = urljoin(base, raw)
        if urlparse(url).scheme not in ("https", "http") or url in seen:
            continue
        seen.add(url)
        yield url, origin

def run(output):
    output.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update(HEADERS)
    results = []
    for key, title, page in SOURCES:
        item = {"id":key,"title":title,"source_url":page,"status":"unavailable",
                "rights_review_required":True,"editorial_approval":False,
                "candidates":[],"selected_image":None}
        try:
            response = session.get(page, timeout=20)
            response.raise_for_status()
            response.encoding = response.apparent_encoding or response.encoding
            for url, origin in list(candidates(response.text, response.url))[:35]:
                attempt = {"url":url,"discovered_via":origin}
                try:
                    r = session.get(url, timeout=18, headers={"Referer":response.url})
                    r.raise_for_status()
                    if len(r.content)>12_000_000:
                        raise ValueError("image exceeds 12MB")
                    im = Image.open(io.BytesIO(r.content))
                    im.load()
                    if im.width<180 or im.height<100:
                        raise ValueError("too small")
                    if im.format not in ("JPEG","PNG","WEBP","GIF"):
                        raise ValueError("unsupported image format")
                    attempt.update({"status":"downloaded","width":im.width,"height":im.height})
                    # Save up to three original page images for manual selection.
                    if sum(x.get("status")=="downloaded" for x in item["candidates"])<3:
                        name = key+"_"+str(sum(x.get("status")=="downloaded" for x in item["candidates"])+1)+".png"
                        im.convert("RGB").save(output/name, format="PNG")
                        attempt["local_file"] = name
                        attempt["sha256"] = hashlib.sha256((output/name).read_bytes()).hexdigest()
                        item["status"] = "candidates_downloaded"
                except Exception as e:
                    attempt.update({"status":"failed","error":str(e)[:160]})
                item["candidates"].append(attempt)
                if sum(x.get("status")=="downloaded" for x in item["candidates"])>=3:
                    break
        except Exception as e:
            item["error"] = str(e)[:250]
        results.append(item)
        print(key, item["status"], flush=True)
    (output/"image_manifest.json").write_text(json.dumps({"edition":"030","date":"2026-10-27","note":"Downloaded images are candidates only; no automatic publishing or rights approval.","items":results},ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# VOL.030 원문 이미지 수집 결과","","다운로드된 이미지는 후보 파일입니다. 기사 연관성과 사용 허가 확인 전 HTML에 삽입하지 마세요.",""]
    for item in results:
        downloaded=[x for x in item["candidates"] if x.get("local_file")]
        lines += ["## "+item["title"],"- 상태: "+item["status"],"- 원문: "+item["source_url"],"- 후보: "+(", ".join(x["local_file"] for x in downloaded) if downloaded else "없음"),"- 편집 승인: 미완료",""]
    (output/"image_report.md").write_text("\n".join(lines),encoding="utf-8")
    print("Downloaded candidates:",sum(bool(x.get("local_file")) for i in results for x in i["candidates"]))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="output/vol030_images")
    run(Path(p.parse_args().output))

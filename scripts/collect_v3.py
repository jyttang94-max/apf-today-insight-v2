
import datetime as dt
import email.utils
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")
NOW = dt.datetime.now(KST)
DATA = Path(__file__).resolve().parents[1] / "data" / "v3"
DATA.mkdir(parents=True, exist_ok=True)

QUERIES = {
    "인재육성·학술연구": [
        "인문학 연구지원 재단",
        "인문사회 학술연구 지원사업",
        "연구자 육성 학술재단",
        "학술연구 성과 출판",
        "해외 인문학 연구지원 재단",
    ],
    "문화예술": [
        "문화재단 예술가 지원",
        "미술관 박물관 전시 연구",
        "문화예술 지원사업",
        "문화예술 접근성",
        "해외 미술관 예술지원 재단",
    ],
    "청년지원": [
        "청년재단 지원사업",
        "청년 인재육성 장학",
        "청년 문화예술 지원",
        "청년 교육 자립 지원",
    ],
    "여성의 삶": [
        "여성 삶 돌봄 연구",
        "여성 예술가 전시",
        "여성 역사 문화 기록",
        "여성 연구자 지원",
    ],
    "아름다움의 의미": [
        "미학 아름다움 연구",
        "아름다움 예술철학",
        "미의 역사 문화",
        "신체 다양성 미학",
    ],
}

EXCLUDE_TERMS = (
    "부고", "로또", "코스피",
    "주가 급등", "연예인 열애",
)


def read_json(name, default):
    try:
        return json.loads(
            (DATA / name).read_text(encoding="utf-8")
        )
    except (OSError, ValueError):
        return default


def write_json(name, value):
    path = DATA / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def article_id(title):
    normalized = re.sub(
        r"[^0-9a-z가-힣]", "", title.lower()
    )
    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()[:20]


def next_business_day(day):
    return day + dt.timedelta(
        days=3 if day.weekday() == 4 else 1
    )


def fetch_rss(query):
    q = urllib.parse.quote(query + " when:7d")
    url = (
        "https://news.google.com/rss/search"
        f"?q={q}&hl=ko&gl=KR&ceid=KR:ko"
    )
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(
        request, timeout=15
    ) as response:
        return ET.fromstring(response.read(2000000))


def resolve_original_url(rss_url):
    """RSS 링크에서 실제 언론사 URL을 확인합니다."""
    try:
        request = urllib.request.Request(
            rss_url,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(
            request, timeout=10
        ) as response:
            final_url = response.geturl()

        parsed = urllib.parse.urlparse(final_url)
        host = (parsed.hostname or "").lower()

        if parsed.scheme not in ("http", "https"):
            return None
        if not host or host == "localhost":
            return None
        if host == "news.google.com":
            return None
        if host.endswith(".google.com"):
            return None

        return final_url
    except Exception:
        return None


def parse_article(item, category):
    title = html.unescape(
        (item.findtext("title") or "").strip()
    )
    source = (item.findtext("source") or "").strip()
    link = (item.findtext("link") or "").strip()

    if source and title.endswith(" - " + source):
        title = title[:-(len(source) + 3)]

    try:
        published = email.utils.parsedate_to_datetime(
            item.findtext("pubDate")
        ).astimezone(KST)
    except (TypeError, ValueError, AttributeError):
        return None

    if not title or not link:
        return None

    if any(term in title for term in EXCLUDE_TERMS):
        return None

    if not (
        NOW - dt.timedelta(days=7)
        <= published
        <= NOW + dt.timedelta(hours=2)
    ):
        return None

    original_url = resolve_original_url(link)

    return {
        "id": article_id(title),
        "title": title,
        "category": category,
        "source": source,
        "published_at": published.isoformat(
            timespec="minutes"
        ),
        "rss_url": link,
        "original_url": original_url,
        "link_resolution_status": (
            "resolved" if original_url else "unresolved"
        ),
        "original_url_verified": False,
        "body_verified": False,
        "status": "원문 본문 대조 필요",
    }


def main():
    morning = NOW.hour < 12
    edition = (
        NOW.date()
        if morning
        else next_business_day(NOW.date())
    )

    previous = read_json("latest.json", {})
    if previous.get("edition_date") == edition.isoformat():
        articles = {
            item["id"]: item
            for item in previous.get("articles", [])
        }
    else:
        articles = {}

    published = set(read_json("published_ids.json", []))
    excluded = set(read_json("excluded_ids.json", []))

    articles = {
        key: item
        for key, item in articles.items()
        if key not in published and key not in excluded
    }

    errors = []
    counts = {
        "rss_items": 0,
        "duplicate_title": 0,
        "excluded": 0,
        "new_articles": 0,
    }

    for category, queries in QUERIES.items():
        for query in queries:
            try:
                feed = fetch_rss(query)

                for item in feed.findall(
                    "./channel/item"
                )[:30]:
                    article = parse_article(item, category)
                    if article is None:
                        continue

                    counts["rss_items"] += 1
                    key = article["id"]

                    if key in published or key in excluded:
                        counts["excluded"] += 1
                        continue

                    if key in articles:
                        counts["duplicate_title"] += 1
                        continue

                    articles[key] = article
                    counts["new_articles"] += 1

            except Exception as error:
                errors.append({
                    "query": query,
                    "error": str(error)[:160],
                })

    result = sorted(
        articles.values(),
        key=lambda item: item["published_at"],
        reverse=True,
    )

    payload = {
        "generated_at": NOW.isoformat(
            timespec="seconds"
        ),
        "edition_date": edition.isoformat(),
        "phase": (
            "08:00_review"
            if morning
            else "16:00_collection"
        ),
        "count": len(result),
        "target_count": 20,
        "verified_count": 0,
        "counts": counts,
        "articles": result,
        "errors": errors,
        "note": (
            "원문 URL은 리다이렉트 기반 잠정 링크입니다. "
            "본문 대조는 뉴스레터 제작 단계에서 별도 수행합니다. "
            "본문 검증 전 기사는 발행에 사용하지 않습니다."
        ),
    }

    write_json("latest.json", payload)

    seen = read_json("seen.json", {})
    for article in result:
        seen[article["id"]] = article["published_at"]
    write_json("seen.json", seen)

    history_name = (
        "history/"
        + NOW.strftime("%Y-%m-%d_%H%M")
        + ".json"
    )
    write_json(history_name, {
        "generated_at": payload["generated_at"],
        "edition_date": payload["edition_date"],
        "candidate_ids": [
            article["id"] for article in result
        ],
        "counts": counts,
        "errors": errors,
    })

    rows = []
    for article in result:
        url = (
            article["original_url"]
            or article["rss_url"]
        )
        rows.append(
            "<tr><td>"
            + html.escape(article["published_at"])
            + "</td><td>"
            + html.escape(article["category"])
            + "</td><td><a href='"
            + html.escape(url, quote=True)
            + "'>"
            + html.escape(article["title"])
            + "</a></td><td>"
            + html.escape(article["source"])
            + "</td><td>"
            + html.escape(
                article["link_resolution_status"]
            )
            + "</td></tr>"
        )

    page = (
        "<!doctype html><html lang='ko'>"
        "<meta charset='utf-8'>"
        "<title>APF TODAY INSIGHT V3 후보보드</title>"
        "<style>"
        "body{font:15px system-ui;"
        "max-width:1100px;margin:30px auto}"
        "td,th{padding:9px;"
        "border-bottom:1px solid #ddd;text-align:left}"
        "</style>"
        "<h1>APF TODAY INSIGHT V3 후보보드</h1>"
        "<p>발행 대상일: "
        + edition.isoformat()
        + " / 수집 시각: "
        + html.escape(payload["generated_at"])
        + " / 후보: "
        + str(len(result))
        + "건</p>"
        "<table><tr>"
        "<th>발행일</th><th>분야</th>"
        "<th>제목</th><th>출처</th>"
        "<th>원문 링크 상태</th>"
        "</tr>"
        + "".join(rows)
        + "</table></html>"
    )

    (DATA / "latest.html").write_text(
        page, encoding="utf-8"
    )

    print(
        "Edition:", edition,
        "Candidates:", len(result),
        "Resolved URLs:", sum(
            bool(a["original_url"]) for a in result
        ),
        "Errors:", len(errors),
    )


if __name__ == "__main__":
    main()

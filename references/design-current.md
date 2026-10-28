# 최종 승인 디자인 및 아카이브 운영 / 2026-10-29

사용자가 확정한 VOL.032 수정본이 단일 디자인 기준이다. assets/master-current.html을 복제하고 콘텐츠만 교체한다. 이전 VOL.019, VOL.024 및 10월28일 지침과 충돌하면 이 문서가 우선한다.

- WHY IT MATTERS는 상단 여성/아름다움 및 세 본문 기사에서 제목과 해설 블록 전체를 삭제한 상태를 유지한다. 새 호에서 복원하지 않는다.
- 기사 구분선은 학술 아래, 문화예술 아래 2곳만 유지한다. 2px #aebbc5 별도 table row로 구현한다. 청년지원 뒤 FROM NEWS TO INSIGHT 바로 위에는 선을 넣지 않는다.
- 美리보기 하단 출처에서 책 제목은 반복하지 않는다. 저자 / 출판사, 연도 / 『아시아의 美』 권수 / 굵은 도서 소개 링크는 유지한다. 본문에 등장하는 책 제목은 유지한다.
- 680px 캔버스와 기존 헤더, 흰 글자/아이콘, 폰트, 여백, 푸터를 유지한다. TODAY IN NUMBERS 및 삭제한 헤더 설명은 복원하지 않는다.
- 여성의 삶/아름다움은 이미지 없는 상단 2열, 다음은 인재육성 및 학술연구, 문화예술, 청년지원, FROM NEWS TO INSIGHT, EDITOR’S PICKS, 美리보기, 의견 CTA, 지난 뉴스레터 순서다.
- 본문 이미지 실제 픽셀과 HTML 규격 278x150, EDITOR 230x189, 책118x157. 본문 td valign=middle 및 vertical-align:middle, 간격20px. 포스터는 확대 후 실제 크롭한다. 제목/주요 피사체가 알아볼 수 있는지 확인한다.
- 요약은 원문 사실을 충실히 전달하고 이미지 높이와 균형을 검토한다. 출처 및 도서 링크 font-weight:700을 유지한다.
- 새 호는 기사, 이미지, 날짜, VOL, 인사이트, 책 정보를 모두 검증하고 교체한다. 이전 호 사진과 URL을 재사용하지 않는다. 실제 Outlook 수신 여부는 별도로 기록한다.

## 매 호 아카이브 갱신 필수
사용자는 2026-10-29 새 VOL 제작 때마다 지난 뉴스레터 보기를 함께 갱신하도록 상시 승인했다. 아카이브 갱신을 별도 요청 대기로 남기지 않는다.
1. 기존 Site https://apf-insight-archive.amoreji.chatgpt.site (project_id appgprj_6ac6eb8f06a08191a8b49ce2717aa8b8) 소스를 최신으로 연다.
2. dist/issues/volNNN.html에 실제 제작 HTML을 추가/교체한다. publication-registry.json에 호수, 날짜, 제목, URL, 원본파일명, edition_status, delivery_status를 기록한다. 동일 VOL은 중복 생성하지 않는다.
3. scripts/rebuild_archive.py로 목록, archive.json, published.json을 함께 갱신하고 VOL 내림차순으로 배포한다.
4. 실제 목록 표시와 HTML URL 연결, 파일 해시를 확인한다. 실패 시 제작 완료와 아카이브 미반영을 구분해 보고한다.
5. archive의 published는 웹 게시 상태다. 검토본은 edition_status=review, 실제 이메일 발송 미확인은 delivery_status=not_verified로 기록한다. 제작/웹 등록만으로 이메일 발송 완료를 주장하지 않는다.
6. 당일 사용자 승인본을 자동 제작의 다른 검토본으로 덮어쓰지 않는다. 현재 확정 호수032 다음 제작은 실제 발행일과 목록을 확인해 결정한다.

## 수집 경로
GitHub 기본 브랜치 트리를 조회해 data/v5/runs/*/candidates.json 중 당일 edition_date에 해당하는 최신 morning_merge를 우선한다. 없으면 확보 시각을 명시한다. 과거 data/latest.json을 현재 수집분으로 간주하지 않는다. 기발행/아카이브 기사와 사건 단위로 중복을 검토한다.

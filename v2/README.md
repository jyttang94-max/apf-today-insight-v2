# APF TODAY INSIGHT V2.0 — 실행 계약 (개발 시작)

상태: **V2.0 구축 중**. 기존 V5 수집 워크플로 및 승인 HTML 마스터를 변경하지 않는다.

## 단일 진입점
사용자: "오늘자 뉴스레터 제작해줘"
1. data/v5/runs/*/candidates.json 에서 edition_date와 run metadata가 일치하는 최신 morning_merge 선택. 없다면 실패 상태.
2. 발행 이력: archive publication registry + 실제 발행 HTML을 정규화한 publication registry 단일 원장 구축. 현행 data/published_ids.json은 JSON이 아닌 Python 코드여서 신뢰할 수 없음. data/data/published_ids.json은 빈 배열.
3. 기사마다 원문 URL, 본문 확인, 날짜, 사실, 중복 사건키, 이미지 원본 URL, 권리상태, 실제 이미지 바이트 검증을 기록. 미검증 기사 제외.
4. 원문 기사 또는 공식기관 이미지 확보. 사용자 제공 이미지는 우선. 이미지 미확보 시 검증된 대체 기사 탐색; 임의 사진 금지.
5. 고정 assets/master-current.html을 기반으로 슬롯별 치환. 다른 슬롯의 기존 사진·텍스트를 수정하지 않는다. WHY 블록 금지.
6. 검사: v2/audit_edition.py + 기존 scripts/audit_html.py 및 이미지 QA + 시각 검수.
7. 모든 필수 게이트 통과 시에만 FINAL 생성. 미통과 시 REVIEW와 문제 목록. 이메일 발송과 HTML 제작을 구분.
8. 승인 후 아카이브 갱신. 사용자가 명시적으로 요청하지 않으면 이메일을 발송하지 않는다.

## 데이터 계약
v2/edition.schema.json을 준수하는 v2/editions/VOLNNN.json을 매 호 작성한다.
verified 기사에는 원문 검증 근거 및 실제 이미지 연결 기록 필수.
book_cover는 재단 공식 이미지 우선, 불가 시 근거와 상태 기록.
수집, 검증, 이미지, 렌더링, QA 단계는 독립 실행 및 재시도 가능해야 한다.

## 단계별 구현
Phase 1: 스키마 및 검사기 (본 커밋)
Phase 2: 기사 원문 검증 및 발행 이력 통합
Phase 3: 이미지 수집 및 콘텐츠 슬롯 기반 HTML 렌더러
Phase 4: PC/모바일 렌더 QA, Outlook 테스트, 아카이브 갱신
Phase 5: 설치된 플러그인 skill.md 단일 진입점으로 통합 및 실제 호출 회귀 테스트

## 완료 조건
명령 한 번으로 동일한 입력은 동일한 검수 결과를 만들고, 미검증 기사가 FINAL에 들어가지 않으며, 이전 기사·이미지가 남지 않고, 5개 이미지 슬롯의 유효성과 매칭이 검증될 것.

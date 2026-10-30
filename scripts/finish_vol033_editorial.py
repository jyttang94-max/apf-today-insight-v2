from pathlib import Path
from bs4 import BeautifulSoup
import base64,io,json
from PIL import Image
p=Path("dist/APF_TODAY_INSIGHT_VOL033_20261030_IMAGE_BUILD.html")
s=BeautifulSoup(p.read_text(encoding="utf-8"),"html.parser")
changes={
"여성의 손작업, 창작과 지식의 역사로 읽다":"이주여성의 마음건강, 지역사회 관계와 교육에 주목",
"니콜 네리그의 『실을 잇는 여자의 손』을 소개한 기사입니다. 직조와 뜨개, 자수를 여성의 지식과 창작의 역사로 읽습니다. 가사나 취미로 여겨졌던 손작업을 자기표현과 정치적 목소리의 통로로 살피며, 여성의 전문성을 바라보는 관점을 넓힙니다.":"이주여성의 마음건강을 개인의 적응 문제만으로 보지 않고 지역사회 관계와 교육 경험을 함께 살피는 보도입니다. 건강 지원과 함께 사회적 연결과 지역사회 참여를 고려할 필요가 있음을 보여줍니다.",
"한국사회복지저널 / 신간 소개 / 10.28 ↗":"헬스경향 / 10.29 ↗",
"박서보와 흐엉 도딘, 서로 다른 비움의 미학":"베트남 칠화에 담긴 고향의 기억과 현대적 표현",
"박서보미술관 개관전을 다룬 비평입니다. 한지에 선을 반복하는 박서보와 얇은 색의 층을 쌓는 흐엉 도딘을 함께 읽습니다. 필자는 문화적 배경과 제작 방식이 다른 두 화면에서 고요와 깊이를 발견하며, 아름다움을 판단하는 기준을 묻습니다.":"베트남 작가 응우옌 응옥 마이는 전통 칠화의 옻칠과 달걀껍질 상감 기법으로 고향 박닌의 관호 민요를 회화에 담습니다. 전통 재료와 지역 문화의 기억을 결합해 현대적 표현으로 확장하는 사례입니다.",
"아트인사이트 / 전시 비평 / 10.28 ↗":"Vietnam.vn / 10.29 ↗",
"국립부경대, 4개국 연구자와 해양인문학 협력 논의":"오뚜기함태호재단, 제35회 학술상에 이영승 교수 선정",
"해역의 역사와 경계인의 삶부터 미래 해양교육까지 다룹니다.":"식품 감각과 소비자과학 연구의 성과를 조명합니다.",
"브릿지경제 / 10.28 ↗":"오뚜기 / 10.29 ↗",
"CJ문화재단, 지원 음악인과 청소년 잇는 재즈위크":"서울문화재단, 예비 청년예술가 22개 팀 무대 지원",
"무료 관람에 초청과 공연 해설을 더한 운영입니다.":"졸업 전후 청년의 실제 공연 경험과 해외 진출을 연결합니다.",
"뉴스핌 / 10.28 ↗":"연합뉴스 / 10.29 ↗",
"청년재단, 지역 이동 청년의 숙박 지원 추진":"삼성, 자립준비청년의 주거부터 취업교육까지 지원",
"우대 서비스와 지역 숙박시설 연계 방안은 준비 단계입니다.":"직무교육과 취업 지원을 결합한 자립 지원 모델입니다.",
"로리더 / 10.28 ↗":"국민일보 / 10.29 ↗",
"무엇을 아름다움의 지식으로 남길 것인가":"지원 이후의 첫 무대, 누가 연결하는가",
"교수신문 / 인터뷰 / 10.28 ↗":"연합뉴스 / 10.29 ↗",
"한국 책 100종을 프랑스어로, 현지 기획의 힘":"예비 예술가의 첫 무대와 다음 기회",
"『논어』에서 읽는 배움과 사랑의 공동체":"전통 장식에서 읽는 동아시아의 아름다움",
"배움과 관계의 아름다움":"일상 공간과 장식의 미적 의미",
"김경희, 진은영 / 서해문집, 2024 / 『아시아의 美』 21권":"박선희 / 서해문집, 2014 / 『아시아의 美』 2권",
}
# Text nodes: exact replacements only, then update paragraphs by their position in source HTML.
for node in list(s.find_all(string=True)):
 t=str(node)
 if t in changes:node.replace_with(changes[t])
texts=list(s.stripped_strings)
def replace_prefix(prefix,new):
 for node in list(s.find_all(string=True)):
  if str(node).strip().startswith(prefix):
   node.replace_with(new);return
 print("SKIP absent old text:",prefix)
replace_prefix("10월 29일 국립부경대","오뚜기함태호재단은 10월 28일 한국식품영양과학회와 공동으로 제35회 학술상 시상식을 열고 단국대 이영승 교수에게 상패와 부상 3,000만 원을 수여했습니다. 식품 감각 평가와 소비자과학 분야의 연구 성과를 조명합니다.")
replace_prefix("CJ문화재단과 재즈피플이","서울문화재단은 서울 커넥트 스테이지 선정 결과를 발표했습니다. 12개 대학 소속 22개 팀, 157명의 예비 청년예술가가 선정됐으며, 2027년 1월부터 3월까지 공연을 선보일 예정입니다. 발표 기회와 해외 협력 프로젝트 연계도 지원합니다.")
replace_prefix("청년재단과 대한숙박업중앙회가","삼성은 자립준비청년을 위한 '삼성희망디딤돌' 사업에서 주거와 정서적 지원에 직무교육과 취업 지원을 더하고 있습니다. 청년이 독립적인 생활 기반을 마련하고 일자리로 이어갈 수 있도록 지원하는 사례입니다.")
replace_prefix("무료 공연을 여는 일과","서울문화재단의 서울 커넥트 스테이지는 예비 청년예술가에게 단순 지원금뿐 아니라 실제 작품 발표 공간을 제공합니다. 12개 대학의 22개 팀이 무대 경험을 쌓고 해외 협력 프로젝트에도 연결될 수 있도록 설계했습니다.")
replace_prefix("두 사례가 던지는 편집상의 질문은","연구자와 창작자의 초기 성과를 지원하는 일과 그 성과가 현장에서 이어지도록 돕는 일은 구분해 볼 필요가 있습니다. 후속 활동을 위한 발표 기회, 네트워크, 외부 기관과의 연결을 지원사업의 운영 요소로 검토할 수 있습니다.")
replace_prefix("APF QUESTION 우리 사업에 참여하고","APF QUESTION 연구비 지원이 끝난 뒤 연구자와 창작자의 다음 활동을 연결하려면 어떤 기회와 협력기관이 필요할까요?")
replace_prefix("프랑스 비영리 출판사","서울문화재단은 예비 청년예술가 22개 팀에 첫 공연 무대를 제공합니다. 단순 선정과 지원을 넘어 전문 활동을 이어갈 기회를 어떻게 설계할지 살펴볼 만합니다.")
replace_prefix("『논어는 아름답다』는","『동아시아 전통 인테리어 장식과 미』는 동아시아의 전통 공간에서 장식과 미적 감각이 어떻게 구현되는지 살펴보는 『아시아의 美』 시리즈 도서입니다. 일상의 공간과 장식에서 문화적 아름다움을 읽어볼 수 있습니다.")
# Change all article anchors including image-parent links by old URL
for a in s.find_all("a",href=True):
 h=a["href"]
 if "ksw-news.com" in h:a["href"]="https://www.google.com/search?q=이주여성+마음건강+헬스경향+2026+10+29"
 if "artinsight.co.kr" in h:a["href"]="https://vietnam.vn/"
 if "viva100.com" in h:a["href"]="https://www.otoki.com/pr/news-detail?idx=1067"
 if "newspim.com" in h:a["href"]="https://www.yna.co.kr/amp/view/AKR20261029179600005"
 if "lawleader.co.kr" in h:a["href"]="https://www.google.com/search?q=삼성희망디딤돌+국민일보+2026+10+29"
 if "kyosu.net" in h:a["href"]="https://www.yna.co.kr/amp/view/AKR20261029179600005"
 if "ascf.amorepacific.co.kr/publishedView.do?seq=115" in h:a["href"]="https://www.yes24.com/product/goods/13866370"
# Explicitly avoid misleading previous image captions
imgs=s.find_all("img")
assert len(imgs)==5
for i,im in enumerate(imgs):
 assert im.get("src","").startswith("data:image/jpeg;base64,")
 b=base64.b64decode(im["src"].split(",",1)[1],validate=True)
 image=Image.open(io.BytesIO(b));image.verify()
for node in list(s.find_all(string=True)):
 t=str(node)
 if "CJ문화재단 제공" in t:node.replace_with("연합뉴스 / 기사 사진")
 if "국립부경대 제공" in t:node.replace_with("오뚜기 공식 홈페이지 이미지")
 if "청년재단과 대한숙박업중앙회 협약식" in t:node.replace_with("국민일보 / 기사 사진")
 if "김봉억 기자 / 교수신문" in t:node.replace_with("연합뉴스 / 기사 사진")
 if "『논어는 아름답다』 표지" in t:node.replace_with("『동아시아 전통 인테리어 장식과 미』 표지")
out=Path("dist/APF_TODAY_INSIGHT_VOL033_20261030_EDITORIAL_IMAGE_REVIEW.html")
out.write_text(str(s),encoding="utf-8")
print("DONE",out,out.stat().st_size,"images",len(imgs))

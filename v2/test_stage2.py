import unittest
from v2.stage2 import classify,canonical_url
class Stage2Tests(unittest.TestCase):
 def setUp(self):
  self.c={"edition_date":"2026-10-30","phase":"evening_collection","articles":[{"id":"a","title":"지원사업 발표","body_verified":False}]}
  self.r={"coverage_complete":True,"records":[]}
  self.e={"a":{"body_verified":True,"original_url":"https://example.org/a","body_evidence_url":"https://example.org/a","verified_at":"2026-10-30T08:00:00+09:00","confirmed_facts":["기관 발표","대상 20명"],"event_key":"program-2026","source_title":"지원사업 발표"}}
 def test_unverified(self):
  self.assertEqual(classify(self.c,self.r,{})["eligible"],0)
 def test_verified(self):
  self.assertEqual(classify(self.c,self.r,self.e)["eligible"],1)
 def test_history_incomplete(self):
  self.r["coverage_complete"]=False
  self.assertEqual(classify(self.c,self.r,self.e)["eligible"],0)
 def test_event_duplicate(self):
  self.r["records"]=[{"title":"별도 제목","edition_date":"2026-10-29","status":"published","event_key":"program-2026"}]
  self.assertIn("PRIOR_EVENT",classify(self.c,self.r,self.e)["results"][0]["reasons"])
 def test_url(self):
  self.assertEqual(canonical_url("https://www.example.org/a?utm_source=foo"),"https://example.org/a")
if __name__=="__main__":unittest.main()

import unittest
from v2.export_editorial_queue import make_queue
class QueueTests(unittest.TestCase):
 def test_unresolved_kept_for_search(self):
  p={"edition_date":"2026-10-30","phase":"evening_collection","articles":[{"id":"x","title":"문화재단 지원 발표","source":"신문사","rss_url":"https://news.google.com/rss/articles/x"}]}
  r={"results":[{"id":"x","status":"unresolved_google_news","original_url":None}]}
  q=make_queue(p,r)
  self.assertEqual(q["total"],1)
  self.assertEqual(q["candidates"][0]["editorial_status"],"needs_independent_search")
  self.assertEqual(q["candidates"][0]["url_resolution_status"],"unresolved_google_news")
 def test_no_automatic_verification(self):
  q=make_queue({"articles":[{"id":"a","title":"A"}]})
  self.assertNotIn("body_verified",q["candidates"][0])
if __name__=="__main__":unittest.main()

import unittest
from v2.editorial_review_report import review
class EditorialReviewTests(unittest.TestCase):
 def test_missing_evidence_held(self):
  r=review({"articles":[{"id":"a","title":"Sample title","source":"X"}]},{},{"records":[]})
  self.assertEqual(r["items"][0]["editorial_status"],"hold")
  self.assertFalse(r["publication_approved"])
 def test_history_title_flag(self):
  r=review({"articles":[{"id":"a","title":"Repeated Story","source":"X"}]},{},{"records":[{"title_hint":"Repeated Story","url":"https://example.org/a"}]})
  self.assertTrue(r["items"][0]["potential_history_duplicate"])
if __name__=="__main__":unittest.main()

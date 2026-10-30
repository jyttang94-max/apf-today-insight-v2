import tempfile,unittest
from pathlib import Path
from v2.build_history_index import index_issues
class HistoryIndexTests(unittest.TestCase):
 def test_html_does_not_imply_published(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"APF_VOL033_20261030_FINAL.html"
   p.write_text('<a href="https://example.org/news/1">Example article headline</a>',encoding="utf-8")
   data=index_issues([str(p)])
   self.assertEqual(data["issues_found"],1)
   self.assertEqual(data["records"][0]["status"],"unconfirmed_issue_link")
   self.assertFalse(data["coverage_complete"])
if __name__=="__main__":unittest.main()

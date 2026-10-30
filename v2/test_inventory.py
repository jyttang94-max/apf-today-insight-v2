import tempfile
import unittest
from pathlib import Path
from v2.inventory_issues import inventory
class InventoryTests(unittest.TestCase):
 def test_html_is_not_published_proof(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"APF_TODAY_INSIGHT_VOL033_20261030_FINAL.html"
   p.write_text('<a href="https://example.org/article">Example headline</a>',encoding="utf-8")
   x=inventory([str(p)])["issues"][0]
   self.assertEqual(x["publication_status"],"unconfirmed")
   self.assertEqual(x["vol"],33)
   self.assertEqual(x["links"][0]["url"],"https://example.org/article")
if __name__=="__main__":unittest.main()

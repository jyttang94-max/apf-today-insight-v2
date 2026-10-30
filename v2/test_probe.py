import io
import unittest
from v2.probe_originals import probe
class Response:
 headers={"Content-Type":"text/html; charset=utf-8"}
 def __enter__(self):return self
 def __exit__(self,*args):return False
 def geturl(self):return "https://example.org/article"
 def read(self,n):return ("<html><title>Actual article</title><article>"+("Verified page text. "*60)+"</article></html>").encode()
class ProbeTests(unittest.TestCase):
 def test_no_original(self):
  x=probe({"id":"a","title":"A","original_url":None})
  self.assertEqual(x["verification_status"],"original_url_missing")
 def test_fetch_not_approval(self):
  x=probe({"id":"a","title":"A","original_url":"https://example.org/article"},lambda _:Response())
  self.assertEqual(x["verification_status"],"retrieved_needs_editor_review")
  self.assertFalse(x["body_verified"])
  self.assertGreater(x["body_length"],500)
if __name__=="__main__":unittest.main()

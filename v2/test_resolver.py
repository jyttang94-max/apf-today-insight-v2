import unittest
from v2.resolve_original_urls import resolve
class Fake:
 def __init__(self,url):self.url=url
 def __enter__(self):return self
 def __exit__(self,*args):return False
 def geturl(self):return self.url
class ResolverTests(unittest.TestCase):
 def test_redirect(self):
  r=resolve({"id":"x","rss_url":"https://news.google.com/rss/articles/abc"},lambda _:Fake("https://publisher.example/article?utm_source=google"))
  self.assertEqual(r["original_url"],"https://publisher.example/article")
  self.assertEqual(r["status"],"redirect_resolved_unverified")
 def test_google_not_original(self):
  r=resolve({"id":"x","rss_url":"https://news.google.com/rss/articles/abc"},lambda _:Fake("https://news.google.com/articles/abc"))
  self.assertIsNone(r["original_url"])
 def test_missing(self):
  self.assertEqual(resolve({"id":"x"})["status"],"missing_google_news_url")
if __name__=="__main__":unittest.main()

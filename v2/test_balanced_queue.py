import unittest
from v2.export_balanced_queue import balanced
class BalancedQueueTests(unittest.TestCase):
 def test_each_category_preserved(self):
  d={"articles":[{"id":str(i),"title":"Story "+str(i),"category":c,"source":"X"} for i,c in enumerate(("인재육성·학술연구","문화예술","청년지원","여성의 삶","아름다움의 의미"))]}
  r=balanced(d)
  self.assertEqual(sum(map(len,r["queues"].values())),5)
  self.assertTrue(all(x["verification_status"]=="unverified" for v in r["queues"].values() for x in v))
if __name__=="__main__":unittest.main()

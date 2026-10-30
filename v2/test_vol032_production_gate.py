import unittest
from v2.vol032_production_gate import preflight
class GateTests(unittest.TestCase):
 def test_partial_never_published(self):
  d={"stories":[{"slot":"academic","body_verified":True,"original_url":"https://example.com/article","body":"Body"}]}
  r=preflight(d)
  self.assertFalse(r["ready_for_full_html"])
  self.assertIn("MISSING_SLOT:arts",r["errors"])
  self.assertIn("HISTORY_NOT_RECONCILED",r["errors"])
if __name__=="__main__":unittest.main()

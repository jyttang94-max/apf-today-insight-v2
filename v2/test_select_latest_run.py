import json,tempfile,unittest
from pathlib import Path
from v2.select_latest_run import select
class LatestRunTests(unittest.TestCase):
 def test_by_timestamp(self):
  with tempfile.TemporaryDirectory() as tmp:
   for name,ts in [("older","2026-10-29T08:00:00+09:00"),("newer","2026-10-30T11:09:18+09:00")]:
    p=Path(tmp)/name/"candidates.json";p.parent.mkdir();p.write_text(json.dumps({"generated_at":ts}))
   self.assertIn("newer",select(tmp))
   self.assertIn("older",select(tmp,"2026-10-30T00:00:00+09:00"))
if __name__=="__main__":unittest.main()

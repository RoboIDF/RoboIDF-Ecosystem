import tempfile
import unittest
from pathlib import Path
from adapter import read_csv, demo
class AdapterTests(unittest.TestCase):
    def test_demo(self):
        with tempfile.TemporaryDirectory() as d:
            r=demo(Path(d));self.assertLess(r['rollout_rmse_m_s'],1e-10)
    def test_invalid_csv(self):
        for body in ['bad,header\n1,2\n','time_s,velocity_m_s,effort_n\n0,0,1\n.1,nan,1\n.2,0,1\n.3,0,\n','time_s,velocity_m_s,effort_n\n0,0,1\n.1,0,1\n.3,0,1\n.4,0,\n']:
            with self.subTest(body=body), tempfile.TemporaryDirectory() as d:
                p=Path(d)/'data.csv';p.write_text(body)
                with self.assertRaises(ValueError): read_csv(p,split='train',seed=0)

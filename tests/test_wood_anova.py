"""Pure-stdlib tests with SYNTHETIC fixtures (not published device measurements)."""
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "tools"))
from wood_anova import f_statistics


class TestFStatistics(unittest.TestCase):
    def test_rejects_insufficient_devices(self):
        with self.assertRaises(ValueError):
            f_statistics([[0.10], [0.20, 0.30]])

    def test_rejects_zero_variance(self):
        with self.assertRaises(ValueError):
            f_statistics([[1, 1, 1], [2, 2, 2]])

    def test_equal_means_yield_zero_F(self):
        out = f_statistics([[1, 2, 3], [2, 1, 3]])
        self.assertAlmostEqual(out["ordinary_f"], 0, places=12)
        self.assertAlmostEqual(out["welch_f"], 0, places=12)
        self.assertEqual(out["ordinary_df"], [1, 4])

    def test_positive_statistics_and_finite_df(self):
        out = f_statistics([[1, 1.5, 2], [3, 4, 5], [6, 7.5, 8]])
        self.assertGreater(out["ordinary_f"], 0)
        self.assertGreater(out["welch_f"], 0)
        self.assertTrue(math.isfinite(out["welch_df"][1]))


if __name__ == "__main__":
    unittest.main()

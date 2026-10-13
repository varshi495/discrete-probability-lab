import unittest
from distributions.binomial import binomial_pmf, binomial_cdf, binomial_stats


class BinomialTests(unittest.TestCase):
    def test_default_statistics(self):
        stats = binomial_stats(20, 0.35)
        self.assertAlmostEqual(stats["mean"], 7.0)
        self.assertAlmostEqual(stats["variance"], 4.55)
        self.assertAlmostEqual(stats["second_moment"], 53.55)

    def test_pmf_sums_to_one(self):
        self.assertAlmostEqual(sum(binomial_pmf(10, 0.4, k) for k in range(11)), 1.0)

    def test_cdf_bounds(self):
        self.assertAlmostEqual(binomial_cdf(10, 0.4, 10), 1.0)
        self.assertAlmostEqual(binomial_cdf(10, 0.4, -1), 0.0)

    def test_edge_probabilities(self):
        self.assertEqual(binomial_pmf(5, 0, 0), 1.0)
        self.assertEqual(binomial_pmf(5, 1, 5), 1.0)


if __name__ == "__main__":
    unittest.main()

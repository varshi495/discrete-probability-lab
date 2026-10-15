import unittest

from app import app
from distributions.binomial import (
    binomial_pmf,
    binomial_cdf,
    binomial_cdf_and_complement,
    binomial_stats,
)


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

    def test_tiny_pmf_remains_nonzero(self):
        self.assertAlmostEqual(binomial_pmf(500, 0.5, 0), 2 ** -500, delta=1e-163)

    def test_cdf_complement_preserves_tiny_upper_tail(self):
        cdf, complement = binomial_cdf_and_complement(100, 0.5, 99)
        self.assertEqual(cdf, 1.0)
        self.assertLess(abs(complement / (2 ** -100) - 1), 1e-12)

    def test_api_returns_accurate_cdf_complement(self):
        response = app.test_client().post(
            "/api/binomial", json={"n": 100, "p": 0.5, "k": 99}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["cdf"], 1.0)
        self.assertLess(abs(response.json["complement"] / (2 ** -100) - 1), 1e-12)

    def test_edge_probabilities(self):
        self.assertEqual(binomial_pmf(5, 0, 0), 1.0)
        self.assertEqual(binomial_pmf(5, 1, 5), 1.0)


if __name__ == "__main__":
    unittest.main()

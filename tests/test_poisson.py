import math
import unittest

from app import app
from distributions.poisson import (
    poisson_cdf,
    poisson_cdf_and_complement,
    poisson_pmf,
    poisson_stats,
)


class PoissonTests(unittest.TestCase):
    def test_default_statistics(self):
        stats = poisson_stats(4)
        self.assertEqual(stats["mean"], 4)
        self.assertEqual(stats["variance"], 4)
        self.assertEqual(stats["standard_deviation"], 2)
        self.assertEqual(stats["second_moment"], 20)
        self.assertEqual(stats["skewness"], 0.5)

    def test_pmf_sums_to_one(self):
        self.assertAlmostEqual(sum(poisson_pmf(4, k) for k in range(30)), 1.0)

    def test_cdf_values_and_bounds(self):
        self.assertAlmostEqual(poisson_cdf(4, 4), 0.6288369352)
        self.assertEqual(poisson_cdf(4, -1), 0.0)
        self.assertEqual(poisson_cdf(0, 0), 1.0)

    def test_zero_rate(self):
        self.assertEqual(poisson_pmf(0, 0), 1.0)
        self.assertEqual(poisson_pmf(0, 1), 0.0)
        self.assertIsNone(poisson_stats(0)["skewness"])

    def test_large_rate_cdf(self):
        self.assertAlmostEqual(poisson_cdf(1000, 1000), 0.5084093672, places=7)

    def test_cdf_complement_preserves_tiny_upper_tail(self):
        cdf, complement = poisson_cdf_and_complement(1, 20)
        expected_complement = math.exp(-1) * sum(
            1 / math.factorial(k) for k in range(21, 50)
        )
        self.assertEqual(cdf, 1.0)
        self.assertAlmostEqual(complement, expected_complement, delta=1e-30)

    def test_poisson_page_and_api(self):
        client = app.test_client()
        self.assertEqual(client.get("/poisson").status_code, 200)
        response = client.post("/api/poisson", json={"lambda": 4, "k": 4})
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(response.json["pmf"], math.exp(-4) * 4 ** 4 / math.factorial(4))
        self.assertAlmostEqual(response.json["cdf"] + response.json["complement"], 1.0)
        self.assertEqual(response.json["stats"]["mean"], 4)
        self.assertGreater(len(response.json["chart"]), 4)

    def test_api_rejects_invalid_inputs(self):
        client = app.test_client()
        for payload in (
            {"lambda": -1, "k": 2},
            {"lambda": 1001, "k": 2},
            {"lambda": 4, "k": 1.5},
            {"lambda": 4, "k": -1},
        ):
            with self.subTest(payload=payload):
                self.assertEqual(client.post("/api/poisson", json=payload).status_code, 400)


if __name__ == "__main__":
    unittest.main()

import unittest

from app import app
from distributions.geometric import (
    geometric_cdf_and_complement,
    geometric_pmf,
    geometric_stats,
)


class GeometricTests(unittest.TestCase):
    def test_default_statistics(self):
        stats = geometric_stats(0.35)
        self.assertAlmostEqual(stats["mean"], 1 / 0.35)
        self.assertAlmostEqual(stats["variance"], 0.65 / 0.35 ** 2)
        self.assertAlmostEqual(stats["second_moment"], 1.65 / 0.35 ** 2)
        self.assertAlmostEqual(stats["skewness"], 1.65 / 0.65 ** 0.5)

    def test_pmf_and_cdf(self):
        self.assertAlmostEqual(geometric_pmf(0.35, 3), 0.35 * 0.65 ** 2)
        cdf, complement = geometric_cdf_and_complement(0.35, 3)
        self.assertAlmostEqual(cdf, 1 - 0.65 ** 3)
        self.assertAlmostEqual(complement, 0.65 ** 3)

    def test_cdf_retains_tiny_complementary_tail(self):
        cdf, complement = geometric_cdf_and_complement(0.35, 200)
        self.assertEqual(cdf, 1.0)
        self.assertAlmostEqual(complement, 0.65 ** 200)

    def test_support_and_degenerate_probability(self):
        self.assertEqual(geometric_pmf(0.35, 0), 0.0)
        self.assertEqual(geometric_pmf(1, 1), 1.0)
        self.assertEqual(geometric_pmf(1, 2), 0.0)
        self.assertEqual(geometric_cdf_and_complement(1, 1), (1.0, 0.0))
        self.assertIsNone(geometric_stats(1)["skewness"])

    def test_invalid_probability(self):
        for p in (0, -0.1, 1.1):
            with self.subTest(p=p):
                with self.assertRaises(ValueError):
                    geometric_pmf(p, 1)

    def test_page_and_api(self):
        client = app.test_client()
        self.assertEqual(client.get("/geometric").status_code, 200)
        self.assertIn(b"Geometric Distribution", client.get("/").data)

        response = client.post("/api/geometric", json={"p": 0.35, "k": 3})
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(response.json["pmf"], 0.35 * 0.65 ** 2)
        self.assertAlmostEqual(response.json["cdf"], 1 - 0.65 ** 3)
        self.assertAlmostEqual(response.json["cdf"] + response.json["complement"], 1)
        self.assertEqual(response.json["chart"][0]["x"], 1)
        tail_response = client.post("/api/geometric", json={"p": 0.35, "k": 200})
        self.assertEqual(tail_response.json["cdf"], 1.0)
        self.assertAlmostEqual(tail_response.json["complement"], 0.65 ** 200)

    def test_api_rejects_invalid_inputs(self):
        client = app.test_client()
        for payload in (
            {"p": 0, "k": 2},
            {"p": 1.1, "k": 2},
            {"p": 0.35, "k": 1.5},
            {"p": 0.35, "k": -1},
        ):
            with self.subTest(payload=payload):
                self.assertEqual(client.post("/api/geometric", json=payload).status_code, 400)


if __name__ == "__main__":
    unittest.main()

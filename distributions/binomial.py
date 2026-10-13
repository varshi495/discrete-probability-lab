import math


def binomial_pmf(n: int, p: float, k: int) -> float:
    """Return P(X=k) for X ~ Binomial(n,p)."""
    if k < 0 or k > n:
        return 0.0
    if p == 0:
        return 1.0 if k == 0 else 0.0
    if p == 1:
        return 1.0 if k == n else 0.0
    return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))


def binomial_cdf(n: int, p: float, k: int) -> float:
    """Return P(X<=k) for X ~ Binomial(n,p)."""
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    return min(1.0, sum(binomial_pmf(n, p, i) for i in range(k + 1)))


def binomial_stats(n: int, p: float) -> dict:
    mean = n * p
    variance = n * p * (1 - p)
    sd = math.sqrt(variance)
    return {
        "mean": mean,
        "variance": variance,
        "standard_deviation": sd,
        "second_moment": variance + mean ** 2,
        "skewness": None if variance == 0 else (1 - 2 * p) / sd,
    }

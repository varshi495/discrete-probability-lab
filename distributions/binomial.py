import math


def binomial_pmf(n: int, p: float, k: int) -> float:
    """Return P(X=k) for X ~ Binomial(n,p)."""
    if k < 0 or k > n:
        return 0.0
    if p == 0:
        return 1.0 if k == 0 else 0.0
    if p == 1:
        return 1.0 if k == n else 0.0
    log_probability = (
        math.lgamma(n + 1)
        - math.lgamma(k + 1)
        - math.lgamma(n - k + 1)
        + k * math.log(p)
        + (n - k) * math.log1p(-p)
    )
    return math.exp(log_probability)


def binomial_cdf(n: int, p: float, k: int) -> float:
    """Return P(X<=k) for X ~ Binomial(n,p)."""
    return binomial_cdf_and_complement(n, p, k)[0]


def binomial_cdf_and_complement(n: int, p: float, k: int) -> tuple[float, float]:
    """Return P(X<=k) and P(X>k), summing the smaller tail directly."""
    if k < 0:
        return 0.0, 1.0
    if k >= n:
        return 1.0, 0.0
    if p == 0:
        return 1.0, 0.0
    if p == 1:
        return 0.0, 1.0

    if k < n * p:
        probability = binomial_pmf(n, p, k)
        lower_tail = [probability]
        for current in range(k, 0, -1):
            probability *= current * (1 - p) / ((n - current + 1) * p)
            lower_tail.append(probability)
        cdf = min(1.0, math.fsum(lower_tail))
        return cdf, max(0.0, 1.0 - cdf)

    first = k + 1
    probability = binomial_pmf(n, p, first)
    upper_tail = [probability]
    for current in range(first, n):
        probability *= (n - current) * p / ((current + 1) * (1 - p))
        upper_tail.append(probability)
    complement = min(1.0, math.fsum(upper_tail))
    return max(0.0, 1.0 - complement), complement


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

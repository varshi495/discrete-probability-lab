import math


def poisson_pmf(rate: float, k: int) -> float:
    """Return P(X=k) for X ~ Poisson(rate)."""
    if rate < 0:
        raise ValueError("Rate must be non-negative.")
    if k < 0:
        return 0.0
    if rate == 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(-rate + k * math.log(rate) - math.lgamma(k + 1))


def poisson_cdf(rate: float, k: int) -> float:
    """Return P(X<=k) for X ~ Poisson(rate)."""
    if rate < 0:
        raise ValueError("Rate must be non-negative.")
    if k < 0:
        return 0.0
    if rate == 0:
        return 1.0

    if k < rate:
        probability = poisson_pmf(rate, k)
        total = probability
        current = k
        while current > 0:
            probability *= current / rate
            total += probability
            current -= 1
            if probability <= total * 1e-15:
                break
        return min(1.0, total)

    probability = poisson_pmf(rate, k + 1)
    tail = probability
    current = k + 1
    while probability > 0:
        current += 1
        probability *= rate / current
        tail += probability
        if probability <= tail * 1e-15:
            break
    return max(0.0, min(1.0, 1.0 - tail))


def poisson_stats(rate: float) -> dict:
    if rate < 0:
        raise ValueError("Rate must be non-negative.")
    return {
        "mean": rate,
        "variance": rate,
        "standard_deviation": math.sqrt(rate),
        "second_moment": rate + rate ** 2,
        "skewness": None if rate == 0 else 1 / math.sqrt(rate),
    }

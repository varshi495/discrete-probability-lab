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
    return poisson_cdf_and_complement(rate, k)[0]


def poisson_cdf_and_complement(rate: float, k: int) -> tuple[float, float]:
    """Return P(X<=k) and P(X>k), summing the smaller tail directly."""
    if rate < 0:
        raise ValueError("Rate must be non-negative.")
    if k < 0:
        return 0.0, 1.0
    if rate == 0:
        return 1.0, 0.0

    if k < rate:
        probability = poisson_pmf(rate, k)
        lower_tail = [probability]
        total = probability
        current = k
        while current > 0:
            probability *= current / rate
            lower_tail.append(probability)
            total += probability
            current -= 1
            if probability <= total * 1e-16:
                break
        cdf = min(1.0, math.fsum(lower_tail))
        return cdf, max(0.0, 1.0 - cdf)

    probability = poisson_pmf(rate, k + 1)
    upper_tail = [probability]
    total = probability
    current = k + 1
    while probability > 0:
        current += 1
        probability *= rate / current
        upper_tail.append(probability)
        total += probability
        if probability <= total * 1e-16:
            break
    complement = min(1.0, math.fsum(upper_tail))
    return max(0.0, 1.0 - complement), complement


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

import math


def geometric_pmf(p: float, k: int) -> float:
    """Return P(X=k) for X counting trials up to the first success."""
    if not 0 < p <= 1:
        raise ValueError("Probability p must be greater than 0 and at most 1.")
    if k < 1:
        return 0.0
    if p == 1:
        return 1.0 if k == 1 else 0.0
    return math.exp(math.log(p) + (k - 1) * math.log1p(-p))


def geometric_cdf_and_complement(p: float, k: int) -> tuple[float, float]:
    """Return P(X<=k) and P(X>k) for the geometric distribution."""
    if not 0 < p <= 1:
        raise ValueError("Probability p must be greater than 0 and at most 1.")
    if k < 1:
        return 0.0, 1.0
    if p == 1:
        return 1.0, 0.0

    log_tail = k * math.log1p(-p)
    return -math.expm1(log_tail), math.exp(log_tail)


def geometric_stats(p: float) -> dict:
    """Return the first two moments and skewness for the distribution."""
    if not 0 < p <= 1:
        raise ValueError("Probability p must be greater than 0 and at most 1.")
    if p == 1:
        return {
            "mean": 1.0,
            "variance": 0.0,
            "standard_deviation": 0.0,
            "second_moment": 1.0,
            "skewness": None,
        }

    denominator = p * p
    if denominator == 0:
        raise ValueError("Probability p is too small to represent these statistics.")
    try:
        mean = 1 / p
        variance = (1 - p) / denominator
        second_moment = (2 - p) / denominator
    except OverflowError as exc:
        raise ValueError(
            "Probability p is too small to represent these statistics."
        ) from exc
    if not all(math.isfinite(value) for value in (mean, variance, second_moment)):
        raise ValueError("Probability p is too small to represent these statistics.")

    return {
        "mean": mean,
        "variance": variance,
        "standard_deviation": math.sqrt(variance),
        "second_moment": second_moment,
        "skewness": (2 - p) / math.sqrt(1 - p),
    }

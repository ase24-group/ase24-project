"""
Finds the next todo to move from dark to lite using a variable combination of
exploration and exploitation.

Exploration score is not bound between 0-1
Explotation score is bound between 0-1
"""

import math
from statistics import mean
from typing import List
import sys


def sigmoid(x):
    return 1 / (1 + math.exp(-1 * x))


def exploration_score(b: float, r: float) -> float:
    # score = abs(b + r) / abs(b - r + 1e-300)
    score = abs(b + r) / abs(b - r + sys.float_info.min)
    # Bound the score between 0 and 1 using Sigmoid
    # return sigmoid(original_score)
    # if score > 1:
    #     return 1.0
    return score


def exploitation_score(b: float, r: float) -> float:
    return b


def norm(x):
    x_min = 0
    x_max = max(x)
    return [(i - x_min) / (x_max - x_min) for i in x]


def exponentially_weighted_rate(rate_of_change, decay_factor=0.5, lookback=-3):
    rate_of_change = rate_of_change[lookback:]

    weights = [(1 - decay_factor) ** i for i in range(len(rate_of_change) - 1, -1, -1)]
    total_weight = sum(weights)

    # Normalize weights
    # normalized_weights = [weight / total_weight for weight in weights]

    # Calculate exponentially weighted rate
    # weighted_rate = -1 * sum(
    #     rate * weight for rate, weight in zip(rate_of_change, weights)
    # )
    weighted_rate = [weight * rate for rate, weight in zip(rate_of_change, weights)]
    return weighted_rate


def calc_rate_of_change(x):
    rate_of_change = [abs(x[i + 1] - x[i]) for i in range(len(x) - 1)]
    return rate_of_change


# class Scorer:
#     def __init__(self) -> None:
#         self.past_true_ys =


def progressive_score(b: float, r: float, past_true_ys: List[float]) -> float:
    # None for first 2 "epochs"
    if len(past_true_ys) <= 1:
        return exploration_score(b, r)

    past_true_ys = norm(past_true_ys)
    rate_of_change = calc_rate_of_change(past_true_ys)

    want_to_exploit_based_on_roc = exponentially_weighted_rate(
        rate_of_change, lookback=-1
    )[0]
    want_to_exploit_based_on_d2h = 1 - past_true_ys[-1]

    want_to_exploit = (want_to_exploit_based_on_roc + want_to_exploit_based_on_d2h) / 2
    want_to_explore = 1 - want_to_exploit

    return want_to_explore * exploration_score(
        b, r
    ) + want_to_exploit * exploitation_score(b, r)
    # if want_to_explore >= 0.5:
    #     return exploration_score(b, r)
    # else:
    #     return exploitation_score(b, r)


if __name__ == "__main__":
    # ys = [0.6, 0.7, 0.8, 0.8, 0.6, 0.1, 0.1]
    ys = [0.8, 0.7, 0.6, 0.6, 0.4, 0.3, 0.2, 0.2, 0.18, 0.15, 0.14]
    ve = [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.1,
    ]

    for i in range(2, len(ys)):
        ny = norm(ys[:i])
        roc = calc_rate_of_change(ny)

        want_to_exploit_roc = exponentially_weighted_rate(roc, lookback=-1)[0]
        # d2h_comp = 1 - ys[i]
        want_to_exploit_d2h = 1 - ny[-1]

        want_to_exploit = want_to_exploit_roc + want_to_exploit_d2h / 2
        want_to_explore = 1 - want_to_exploit

        print(ny)
        print(want_to_exploit, want_to_explore)

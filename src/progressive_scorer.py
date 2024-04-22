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
from matplotlib import pyplot as plt
from matplotlib.figure import Figure


class ProgressiveScorer:
    def __init__(self, budget: int) -> None:
        self.budget = budget
        self.progress: int = 0

        self.progress_percentage = 0.85

        # Just explore for the first 2 epochs to get enough values in past_true_ys
        self.initial_epochs_to_only_explore: int = 2  # must be >= 2

        self.exponentially_weighted_rate_decay_factor: float = 0.5
        self.exponentially_weighted_rate_lookback: int = 1

        self.past_true_ys: List[float] = []

        self.want_to_explores: List[float] = []
        self.want_to_exploits: List[float] = []

    @staticmethod
    def exploration_score(b: float, r: float) -> float:
        score = abs(b + r) / abs(b - r + sys.float_info.min)
        return score

    @staticmethod
    def exploitation_score(b: float, r: float) -> float:
        return b

    @staticmethod
    def min_norm(x: List[float]) -> List[float]:
        x_min = 0
        x_max = max(x)
        return [(i - x_min) / (x_max - x_min) for i in x]

    def exponentially_weighted_rate(self, rate_of_changes: List[float]) -> List[float]:
        rate_of_changes = rate_of_changes[
            (-1 * self.exponentially_weighted_rate_lookback) :
        ]

        weights = [
            (1 - self.exponentially_weighted_rate_decay_factor) ** i
            for i in range(len(rate_of_changes) - 1, -1, -1)
        ]

        weighted_rates = [
            weight * rate for rate, weight in zip(rate_of_changes, weights)
        ]
        return weighted_rates

    @staticmethod
    def calc_rate_of_change(x: List[float]) -> List[float]:
        rate_of_changes = [abs(x[i + 1] - x[i]) for i in range(len(x) - 1)]
        return rate_of_changes

    def score(self, b: float, r: float) -> float:
        weighted_exploration_score = self.want_to_explores[-1] * exploration_score(b, r)
        weighted_exploitation_score = self.want_to_exploits[-1] * exploitation_score(
            b, r
        )

        return weighted_exploration_score + weighted_exploitation_score

    def add_history(self, y: float) -> None:
        self.past_true_ys.append(y)
        self.progress += 1

        # Just explore for the first x >= 2 epochs to get enough values in past_true_ys
        # Also makes sense to only explore initially
        if len(self.past_true_ys) < self.initial_epochs_to_only_explore:
            want_to_exploit = 0
            want_to_explore = 1
        elif self.progress / self.budget >= self.progress_percentage:
            want_to_exploit = 1
            want_to_explore = 0
        else:
            # Normalize past targets to examine distance from worst explored example
            # The target of the worst example will vary depending on the dataset so it is best
            # to min-normalize
            self.past_true_ys = norm(self.past_true_ys)

            # Calculate the rate of change vector
            rate_of_changes = calc_rate_of_change(self.past_true_ys)

            want_to_exploit_based_on_roc = self.exponentially_weighted_rate(
                rate_of_changes
            )[0]
            want_to_exploit_based_on_d2h = 1 - self.past_true_ys[-1]

            want_to_exploit = (
                want_to_exploit_based_on_roc + want_to_exploit_based_on_d2h
            ) / 2
            want_to_explore = 1 - want_to_exploit

        # For plotting purposes
        self.want_to_explores.append(want_to_explore)
        self.want_to_exploits.append(want_to_exploit)

    def plot_performance(self) -> Figure:
        epochs = range(1, self.budget + 1)

        fig = plt.figure()
        plt.grid()

        plt.scatter(epochs, self.past_true_ys, label="Best D2H", color="blue")

        plt.plot(
            epochs,
            self.want_to_explores,
            label="Want to explore",
            color="green",
            linestyle="--",
        )
        plt.plot(
            epochs,
            self.want_to_exploits,
            label="Want to exploit",
            color="red",
            linestyle="--",
        )

        plt.legend()
        plt.xlabel("Epoch")
        # plt.title("Progressive Acquisition Performance")

        return fig


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


def exponentially_weighted_rate(rate_of_change, decay_factor=0.5, lookback=-1):
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
    # Just explore for the first 2 epochs to get enough values in past_true_ys
    # It also makes sense to just explore initially
    if len(past_true_ys) <= 1:
        return exploration_score(b, r)

    # Normalize past targets to examine distance from worst explored example
    # The target of the worst example will vary depending on the dataset so it is best
    # to min-normalize
    past_true_ys = norm(past_true_ys)

    # Calculate the rate of change vector
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

    want_to_explores = []
    want_to_exploits = []

    for i in range(2, len(ys) - 2):
        ny = norm(ys[:i])
        roc = calc_rate_of_change(ny)

        want_to_exploit_roc = exponentially_weighted_rate(roc, lookback=-1)[0]
        # d2h_comp = 1 - ys[i]
        want_to_exploit_d2h = 1 - ny[-1]

        want_to_exploit = want_to_exploit_roc + want_to_exploit_d2h / 2
        want_to_explore = 1 - want_to_exploit

        want_to_exploits.append(want_to_exploit)
        want_to_explores.append(want_to_explore)

    plt.figure()
    plt.scatter(range(len(ys)), ys)
    plt.plot(range(len(ys)), 2 * [0] + want_to_exploits + 2 * [1])
    plt.plot(range(len(ys)), 2 * [1] + want_to_explores + 2 * [0])
    plt.show()

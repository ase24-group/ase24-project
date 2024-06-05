from utils import get_cumulative_density, get_probability_density
import math


def PI_score(mean, std, best_d2h):
    exploit_explore_tradeoff = (
        0.01  # The paper says that this has to be manually chosen.
    )
    m = (mean - best_d2h - exploit_explore_tradeoff) / std
    score = get_cumulative_density(m, mean, std)
    return score


# Expected improvement score
def EI_score(mean, std, best_d2h):
    exploit_explore_tradeoff = 0.01  # As recommended by Hoffman et al 2011
    m = (mean - best_d2h - exploit_explore_tradeoff) / std
    cum_density_coeff = mean - best_d2h - exploit_explore_tradeoff
    score = (cum_density_coeff * get_cumulative_density(m, mean, std)) + (
        std * get_probability_density(m, mean, std)
    )

    return score


# TODO: check the results for both input dim and overall dim
def UCB_score(mean, std, lite_size, dim):
    delta = 0.1
    v = 1
    gamma = 2 * math.log((lite_size ** (dim / 2 + 2) * math.pi**2) / 3 * delta)
    # revisit the std coeff
    std_coeff = (v * gamma) ** 0.5

    return mean + std_coeff * std

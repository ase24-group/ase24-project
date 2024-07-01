from utils import get_cumulative_density, get_probability_density
import math
import sys


def PI_score(mean, std, best_d2h):
    exploit_explore_tradeoff = (
        0.01  # The paper says that this has to be manually chosen.
    )
    m = (mean - best_d2h - exploit_explore_tradeoff) / (std + sys.float_info.min)
    score = get_cumulative_density(m, mean, std)
    return score


# Expected improvement score
def EI_score(mean, std, best_d2h):
    exploit_explore_tradeoff = 0.01  # As recommended by Hoffman et al 2011
    m = (mean - best_d2h - exploit_explore_tradeoff) / (std + sys.float_info.min)
    cum_density_coeff = mean - best_d2h - exploit_explore_tradeoff
    score = (cum_density_coeff * get_cumulative_density(m, mean, std)) + (
        std * get_probability_density(m, mean, std)
    )

    return score


def get_UCB_coefficients(lite_size, dark_size):
    delta = 0.1
    v = 1
    D = lite_size + dark_size
    # gamma = 2 * math.log((lite_size ** (dim / 2 + 2) * math.pi**2) / 3 * delta)
    gamma = 2 * math.log((D * lite_size**2 * math.pi**2) / 6 * delta)
    # revisit the std coeff
    std_coeff = (v * gamma) ** 0.5

    return std_coeff 

# TODO: check the results for both input dim and overall dim
def UCB_plus_score(mean, std, lite_size, dark_size, dim):
    std_coeff = get_UCB_coefficients(lite_size, dark_size)
    return mean + std_coeff * std

def UCB_minus_score(mean, std, lite_size, dark_size, dim):
    std_coeff = get_UCB_coefficients(lite_size, dark_size)
    return mean - std_coeff * std

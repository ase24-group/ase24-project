from utils import get_cumulative_density
import math

def PI_score(mean, std, best_d2h):
    exploit_explore_tradeoff = 0.01 # The paper says that this has to be manually chosen.
    score = get_cumulative_density((mean - best_d2h - exploit_explore_tradeoff)/std)
    return score

# TODO: check the results for both input dim and overall dim
def UCB_score(mean, std, lite_size, dim):
    delta = 0.1
    v = 1
    gamma = (2 * math.log((lite_size**(dim/2 + 2) * math.pi**2)/3*delta))
    # revisit the std coeff
    std_coeff = (v*gamma)**0.5

    return mean + std_coeff*std

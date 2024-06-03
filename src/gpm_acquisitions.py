from utils import get_cumulative_density

def PI_score(mean, std, best_d2h):
    exploit_exploit_tradeoff = 0.01 # The paper says that this has to be manually chosen.
    score = get_cumulative_density((mean - best_d2h - exploit_exploit_tradeoff)/std)
    return score


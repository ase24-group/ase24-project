from data import Data
from utils import pad_numbers


class TestProject:
    def __init__(self) -> None:
        pass

    def auto93(self) -> None:
        d = Data("../output/params.csv")
        d.training_data = Data("../data/auto93.csv")

        best_config, rest, evals = d.branch()

        print("Centroid of output cluster:")
        print(pad_numbers(best_config.mid().cells), pad_numbers(rest.mid().cells))
        print("Evals: " + str(evals))

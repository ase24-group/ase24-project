import os, random, math
from datetime import datetime
from utils import (
    coerce,
    output,
    output_gate20_info,
    align_list,
    get_filename_and_parent,
)
from data import Data
from box import Box
from num import Num
from config import config
from stats import Sample, eg0
from logger import logger
import sys
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from typing import List


class TestGate:
    def __init__(self):
        pass

    def stats(self):
        # Test stats correct
        stats = output(Data("../data/auto93.csv").stats())
        print(stats)
        return stats == "{.N: 398, Acc+: 15.57, Lbs-: 2970.42, Mpg+: 23.84}"

    def coerce(self):
        # Test string is converted to python dictionary
        dict_ex = coerce("{'a': 1, 'b': 2}")
        print(dict_ex)
        return type(dict_ex) == dict

    def output(self):
        # Test ' is removed from dict for string representation
        out = output({"a": 1, "b": 2})
        print(out)
        return out == "{a: 1, b: 2}"

    def count_classes(self) -> None:
        files = ["diabetes.csv", "soybean.csv"]
        success = True

        for file in files:
            file_name, _ = os.path.splitext(file)
            data = Data(f"../data/{file}")
            class_counts = data.cols.klass.has

            # Number of classes in each file
            number_of_classes = len(class_counts)
            out = f"{file_name}:\n"
            out += f"number of classes: {number_of_classes}\n"

            table_data = list(class_counts.items())
            total_rows = len(data.rows)

            # Max width for each column
            class_column_width = max(
                len(str(class_name)) for class_name, _ in table_data
            )
            count_column_width = max(len(str(count)) for _, count in table_data)
            percent_column = [((count / total_rows) * 100) for _, count in table_data]
            percent_column_width = max(
                len(f"{percent:05.2f} %") for percent in percent_column
            )

            out += "{:<{}}\t{:<{}}\t{:<{}}\n".format(
                "Class",
                class_column_width,
                "Count",
                count_column_width,
                "Percentage",
                percent_column_width,
            )
            for class_name, count in table_data:
                percent = (count / total_rows) * 100
                out += "{:<{}}\t{:<{}}\t{:<{}}\n".format(
                    class_name,
                    class_column_width,
                    count,
                    count_column_width,
                    f"{percent:05.2f} %",
                    percent_column_width,
                )

            print(out)

            with open(
                f"../test_assets/expected_{file_name}_count_classes.txt", "r"
            ) as f:
                if f.read() != out:
                    success = False

        return success

    def bayes(self):
        wme = Box({"acc": 0, "datas": {}, "tries": 0, "n": 0})
        Data("../data/diabetes.csv", lambda data, t: learn(data, t, wme))
        print("Accuracy: ", wme.acc / (wme.tries))
        return wme.acc / (wme.tries) > 0.72

    def km(self):
        print("#{:<4s}\t{}\t{}".format("acc", "k", "m"))
        for k in range(4):
            for m in range(4):
                # if k != 0 or m != 0:
                config.value.k = k
                config.value.m = m
                wme = Box({"acc": 0, "datas": {}, "tries": 0, "n": 0})
                Data("../data/soybean.csv", lambda data, t: learn(data, t, wme))
                print("{:05.2f}%\t{}\t{}".format(wme.acc * 100 / wme.tries, k, m))

    def gate20(self):
        print("#best, mid")
        for i in range(20):
            d = Data("../data/auto93.csv")
            stats, bests, _ = d.gate(4, 16, 0.5)
            stat, best = stats[-1], bests[-1]
            print(f"{round(best.d2h(d), 2)}\t{round(stat.d2h(d), 2)}")

    def gate20_info(self):
        info = {}

        for i in range(20):
            if i != 0:
                # Increment seed by 1 to set a new seed for each run
                config.value.seed += 1
            d = Data("../data/auto93.csv")
            _, _, info = d.gate(4, 10, 0.5, info)

        output_gate20_info(info)

    def smo_no_stats(self):
        date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        file = "../data/auto93.csv"
        repeats = 20

        data = Data(file, fun=None, sortD2H=False)

        label_width = 10
        print(f"date    : {date}")
        print(f"file    : {file}")
        print(f"repeats : {repeats}")
        print(f"seed    : {config.value.seed}")
        print(f"rows    : {len(data.rows)}")
        print(f"cols    : {len(data.cols.names)}")

        # names = f"{'names':{label_width}}{align_list(data.cols.names)}"
        # print(names)
        print(data.cols.names)

        # mid = f"{'mid':{label_width}}{align_list(data.mid().cells)}"
        # print(mid)
        print(data.mid().cells)

        # div = f"{'div':{label_width}}{align_list(data.div().cells)}"
        # print(div)
        print(data.div().cells)

        print("#")

        smo9s = [data.smo(score=lambda b, r: 2 * b - r) for _ in range(repeats)]
        smo9s = sorted(smo9s, key=lambda row: row.d2h(data))
        for row in smo9s:
            # label = f"smo{config.value.budget0 + config.value.Budget}"
            # smo9 = f"{label:{label_width}}{align_list(row.cells)}"
            # print(smo9)
            print(row.cells)

        print("#")

        any50s = []
        for _ in range(repeats):
            random.shuffle(data.rows)
            any50s += [data.clone(data.rows[:50], sortD2H=True).rows[0]]
        for row in sorted(any50s, key=lambda row: row.d2h(data)):
            # label = "any50"
            # any50 = f"{label:{label_width}}{align_list(row.cells)}"
            # print(any50)
            print(row.cells)

        print("#")

        # all = f"{'100%':{label_width}}{align_list(data.clone(data.rows, sortD2H=True).rows[0].cells)}"
        # print(all)

    def smo_stats(self):
        date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        file = "../data/auto93.csv"
        repeats = 20

        data = Data(file, fun=None, sortD2H=False)
        stats = []

        print(f"date    : {date}")
        print(f"file    : {file}")
        print(f"repeats : {repeats}")
        print(f"seed    : {config.value.seed}")
        print(f"rows    : {len(data.rows)}")
        print(f"cols    : {len(data.cols.names)}")

        d2h_values = Num("d2h_values", 0)
        for row in data.clone(data.rows, sortD2H=True).rows:
            d2h_values.add(row.d2h(data))
        print(f"best    : {round(d2h_values.lo, 2)}")
        print(f"tiny    : {round(d2h_values.div() * config.value.cohen, 2)}")
        sorted_d2hs = sorted([row.d2h(data) for row in data.rows])
        print("#base", end=" ")
        stats.append(Sample(sorted_d2hs, txt="base"))

        for budget in [9, 15, 20]:
            config.value.Budget = budget - config.value.budget0
            print("#bonr" + str(budget), end=" ")
            stats.append(
                Sample(
                    [
                        data.smo(
                            score=lambda b, r: abs(b + r)
                            / abs(b - r + sys.float_info.min)
                        ).d2h(data)
                        for _ in range(repeats)
                    ],
                    txt="#bonr" + str(budget),
                )
            )
            print("#rand" + str(budget), end=" ")
            stats.append(
                Sample(
                    [
                        data.clone(shuffle(data.rows[:budget]), sortD2H=True)
                        .rows[0]
                        .d2h(data)
                        for _ in range(repeats)
                    ],
                    txt="#rand" + str(budget),
                )
            )
        print("#rand" + str(int(0.9 * len(data.rows))), end=" ")
        stats.append(
            Sample(
                [
                    data.clone(
                        shuffle(data.rows[: int(0.9 * len(data.rows))]), sortD2H=True
                    )
                    .rows[0]
                    .d2h(data)
                    for _ in range(repeats)
                ],
                txt="#rand" + str(int(0.9 * len(data.rows))),
            )
        )

        print("\n#report" + str(len(stats)))
        eg0(stats)

    def smo_progressive_scorer_no_stats(self):
        date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        file = "../data/auto93.csv"
        repeats = 20

        data = Data(file, fun=None, sortD2H=False)

        label_width = 10
        print(f"date    : {date}")
        print(f"file    : {file}")
        print(f"repeats : {repeats}")
        print(f"seed    : {config.value.seed}")
        print(f"rows    : {len(data.rows)}")
        print(f"cols    : {len(data.cols.names)}")

        # names = f"{'names':{label_width}}{align_list(data.cols.names)}"
        # print(names)
        print(data.cols.names)

        # mid = f"{'mid':{label_width}}{align_list(data.mid().cells)}"
        # print(mid)
        print(data.mid().cells)

        # div = f"{'div':{label_width}}{align_list(data.div().cells)}"
        # print(div)
        print(data.div().cells)

        print("#")

        smo9s = [data.smo_progressive_scorer() for _ in range(repeats)]
        smo9s = sorted(smo9s, key=lambda row: row.d2h(data))
        for row in smo9s:
            label = f"smo{config.value.budget0 + config.value.Budget}"
            # smo9 = f"{label:{label_width}}{align_list(row.cells)}"
            # print(smo9)
            print(row.cells)

        print("#")

        any50s = []
        for _ in range(repeats):
            random.shuffle(data.rows)
            any50s += [data.clone(data.rows[:50], sortD2H=True).rows[0]]
        for row in sorted(any50s, key=lambda row: row.d2h(data)):
            label = "any50"
            # any50 = f"{label:{label_width}}{align_list(row.cells)}"
            # print(any50)
            print(row.cells)

        print("#")

        # all = f"{'100%':{label_width}}{align_list(data.clone(data.rows, sortD2H=True).rows[0].cells)}"
        # print(all)

    def smo_progressive_scorer_stats(self):
        date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        file = "../data/coc10000.csv"
        repeats = 20

        data = Data(file, fun=None, sortD2H=False)
        stats = []

        print(f"date    : {date}")
        print(f"file    : {file}")
        print(f"repeats : {repeats}")
        print(f"seed    : {config.value.seed}")
        print(f"rows    : {len(data.rows)}")
        print(f"cols    : {len(data.cols.names)}")

        d2h_values = Num("d2h_values", 0)
        for row in data.clone(data.rows, sortD2H=True).rows:
            d2h_values.add(row.d2h(data))
        print(f"best    : {round(d2h_values.lo, 2)}")
        print(f"tiny    : {round(d2h_values.div() * config.value.cohen, 2)}")
        sorted_d2hs = sorted([row.d2h(data) for row in data.rows])
        print("#base", end=" ")
        stats.append(Sample(sorted_d2hs, txt="base"))

        # Use formulas to compute the budgets
        for budget in [9, 15, math.ceil(math.sqrt(len(data.rows)))]:
            config.value.Budget = budget - config.value.budget0

            random.seed(config.value.seed)
            logger.info("Progressive")
            print("#progressive" + str(budget), end=" ")
            stats.append(
                Sample(
                    [data.smo_progressive_scorer().d2h(data) for _ in range(repeats)],
                    txt="#progressive" + str(budget),
                )
            )

            random.seed(config.value.seed)
            logger.info("SimAnnealing")
            print("#SimAnnealing" + str(budget), end=" ")
            stats.append(
                Sample(
                    [data.smo_sim_annealing().d2h(data) for _ in range(repeats)],
                    txt="#SimAnnealing" + str(budget),
                )
            )

            random.seed(config.value.seed)
            logger.info("bonr")
            print("#bonr" + str(budget), end=" ")
            stats.append(
                Sample(
                    [
                        data.smo(
                            score=lambda b, r: abs(b + r)
                            / abs(b - r + sys.float_info.min)
                        ).d2h(data)
                        for _ in range(repeats)
                    ],
                    txt="#bonr" + str(budget),
                )
            )

            # random.seed(config.value.seed)
            # print("#progressive" + str(budget), end=" ")
            # stats.append(
            #     Sample(
            #         [
            #             data.smo(
            #                 score=lambda b, r: abs(b + r)
            #                 / abs(b - r + sys.float_info.min)
            #             ).d2h(data)
            #             for _ in range(repeats)
            #         ],
            #         txt="#progressive" + str(budget),
            #     )
            # )

            random.seed(config.value.seed)
            print("#rand" + str(budget), end=" ")
            stats.append(
                Sample(
                    [
                        data.clone(shuffle(data.rows[:budget]), sortD2H=True)
                        .rows[0]
                        .d2h(data)
                        for _ in range(repeats)
                    ],
                    txt="#rand" + str(budget),
                )
            )

        random.seed(config.value.seed)
        print("#rand" + str(int(0.9 * len(data.rows))), end=" ")
        stats.append(
            Sample(
                [
                    data.clone(
                        shuffle(data.rows[: int(0.9 * len(data.rows))]), sortD2H=True
                    )
                    .rows[0]
                    .d2h(data)
                    for _ in range(repeats)
                ],
                txt="#rand" + str(int(0.9 * len(data.rows))),
            )
        )

        print("\n#report" + str(len(stats)))
        random.shuffle(stats)
        eg0(stats)

    def base_stats(self):
        data = Data(config.value.file, fun=None, sortD2H=False)
        sorted_d2hs = sorted([row.d2h(data) for row in data.rows])

        csv_filename, csv_parent_folder = get_filename_and_parent(config.value.file)
        stats_dir = f"../results/stats/{csv_parent_folder}/{csv_filename}"
        treatment = "base"
        os.makedirs(stats_dir, exist_ok=True)

        with open(f"{stats_dir}/{treatment}.txt", "w") as file:
            file.write(f"{treatment} {' '.join(map(str, sorted_d2hs))}")

    def progressive_stats(self):
        data = Data(config.value.file, fun=None, sortD2H=False)
        repeats = 20

        budget = config.value.ExpBudget
        config.value.Budget = budget - config.value.budget0

        csv_filename, csv_parent_folder = get_filename_and_parent(config.value.file)
        csv_budget = math.ceil(math.sqrt(len(data.rows)))
        stats_dir = f"../results/stats/{csv_parent_folder}/{csv_filename}"
        plots_dir = f"../results/plots/{csv_parent_folder}/{csv_filename}"
        treatment = f"progressive_{str(budget)}"
        if budget == csv_budget:
            treatment = f"progressive_sqrt"
        os.makedirs(stats_dir, exist_ok=True)
        os.makedirs(plots_dir, exist_ok=True)

        stats = []
        best_repeat = 1
        best_fig = None

        for _ in range(repeats):
            best_d2h, progressive_scorer = data.smo_progressive_scorer()
            best_d2h = best_d2h.d2h(data)
            stats.append(best_d2h)

            if best_d2h < best_repeat:
                best_fig = progressive_scorer.plot_performance()

        best_fig.savefig(f"{plots_dir}/{treatment}.png")

        # stats = [data.smo_progressive_scorer().d2h(data) for _ in range(repeats)]
        with open(f"{stats_dir}/{treatment}.txt", "w") as file:
            file.write(f"{treatment} {' '.join(map(str, stats))}")

    def SimAnnealing_stats(self):
        data = Data(config.value.file, fun=None, sortD2H=False)
        repeats = 20

        budget = config.value.ExpBudget
        config.value.Budget = budget - config.value.budget0

        csv_filename, csv_parent_folder = get_filename_and_parent(config.value.file)
        csv_budget = math.ceil(math.sqrt(len(data.rows)))
        stats_dir = f"../results/stats/{csv_parent_folder}/{csv_filename}"
        plots_dir = f"../results/plots/{csv_parent_folder}/{csv_filename}"
        treatment = f"SimAnnealing_{str(budget)}"
        if budget == csv_budget:
            treatment = f"SimAnnealing_sqrt"
        os.makedirs(stats_dir, exist_ok=True)
        os.makedirs(plots_dir, exist_ok=True)

        # stats = [data.smo_sim_annealing().d2h(data) for _ in range(repeats)]
        stats = []
        sampled_d2h_history = {}
        b_exp_values = None

        trials_to_plot = [0, 4, 9, 14, 19]

        for trial in range(repeats):
            best_d2h, d2h_history, b_exp_values = data.smo_sim_annealing()
            best_d2h = best_d2h.d2h(data)
            stats.append(best_d2h)

            if trial in trials_to_plot:
                sampled_d2h_history[trial] = d2h_history

        sim_annealing_plot_performance(
            config.value.Budget, sampled_d2h_history, b_exp_values
        ).savefig(f"{plots_dir}/{treatment}.png")

        with open(f"{stats_dir}/{treatment}.txt", "w") as file:
            file.write(f"{treatment} {' '.join(map(str, stats))}")

    def ExpProgressive_stats(self):
        data = Data(config.value.file, fun=None, sortD2H=False)
        repeats = 20

        budget = config.value.ExpBudget
        config.value.Budget = budget - config.value.budget0

        csv_filename, csv_parent_folder = get_filename_and_parent(config.value.file)
        csv_budget = math.ceil(math.sqrt(len(data.rows)))
        stats_dir = f"../results/stats/{csv_parent_folder}/{csv_filename}"
        plots_dir = f"../results/plots/{csv_parent_folder}/{csv_filename}"
        treatment = f"ExpProgressive_{str(budget)}"
        if budget == csv_budget:
            treatment = f"ExpProgressive_sqrt"
        os.makedirs(stats_dir, exist_ok=True)
        os.makedirs(plots_dir, exist_ok=True)

        stats = []
        sampled_d2h_history = {}

        trials_to_plot = [0, 4, 9, 14, 19]

        for trial in range(repeats):
            best_d2h, d2h_history, want_to_exploits = data.smo_exp_progressive()
            best_d2h = best_d2h.d2h(data)
            stats.append(best_d2h)

            if trial in trials_to_plot:
                sampled_d2h_history[trial] = d2h_history

        exp_progressive_plot_performance(
            config.value.Budget, sampled_d2h_history, want_to_exploits
        ).savefig(f"{plots_dir}/{treatment}.png")

        with open(f"{stats_dir}/{treatment}.txt", "w") as file:
            file.write(f"{treatment} {' '.join(map(str, stats))}")

    # Probability of Improvement acquisition function: usually used in Gaussian Process Models (GPM)
    def PI_stats(self):
        data = Data(config.value.file, fun=None, sortD2H=False)
        repeats = 20

        budget = config.value.ExpBudget
        config.value.Budget = budget - config.value.budget0

        csv_filename, csv_parent_folder = get_filename_and_parent(config.value.file)
        csv_budget = math.ceil(math.sqrt(len(data.rows)))
        stats_dir = f"../results/stats/{csv_parent_folder}/{csv_filename}"
        plots_dir = f"../results/plots/{csv_parent_folder}/{csv_filename}"
        treatment = f"PI_{str(budget)}"
        if budget == csv_budget:
            treatment = f"PI_sqrt"
        os.makedirs(stats_dir, exist_ok=True)
        os.makedirs(plots_dir, exist_ok=True)

        stats = []
        sampled_d2h_history = {}

        trials_to_plot = [0, 4, 9, 14, 19]

        for trial in range(repeats):
            best_d2h, d2h_history = data.smo_GP()
            best_d2h = best_d2h.d2h(data)
            stats.append(best_d2h)

            if trial in trials_to_plot:
                sampled_d2h_history[trial] = d2h_history

        smo_plot_performance(config.value.Budget, sampled_d2h_history).savefig(
            f"{plots_dir}/{treatment}.png"
        )

        with open(f"{stats_dir}/{treatment}.txt", "w") as file:
            file.write(f"{treatment} {' '.join(map(str, stats))}")

    def bonr_stats(self):
        data = Data(config.value.file, fun=None, sortD2H=False)
        repeats = 20

        budget = config.value.ExpBudget
        config.value.Budget = budget - config.value.budget0

        csv_filename, csv_parent_folder = get_filename_and_parent(config.value.file)
        csv_budget = math.ceil(math.sqrt(len(data.rows)))
        stats_dir = f"../results/stats/{csv_parent_folder}/{csv_filename}"
        plots_dir = f"../results/plots/{csv_parent_folder}/{csv_filename}"
        treatment = f"bonr_{str(budget)}"
        if budget == csv_budget:
            treatment = f"bonr_sqrt"
        os.makedirs(stats_dir, exist_ok=True)
        os.makedirs(plots_dir, exist_ok=True)

        stats = []
        sampled_d2h_history = {}

        trials_to_plot = [0, 4, 9, 14, 19]

        for trial in range(repeats):
            best_d2h, d2h_history = data.smo(
                score=lambda b, r: abs(b + r) / abs(b - r + sys.float_info.min)
            )
            best_d2h = best_d2h.d2h(data)
            stats.append(best_d2h)

            if trial in trials_to_plot:
                sampled_d2h_history[trial] = d2h_history

        smo_plot_performance(config.value.Budget, sampled_d2h_history).savefig(
            f"{plots_dir}/{treatment}.png"
        )

        with open(f"{stats_dir}/{treatment}.txt", "w") as file:
            file.write(f"{treatment} {' '.join(map(str, stats))}")

    def b2_stats(self):
        data = Data(config.value.file, fun=None, sortD2H=False)
        repeats = 20

        budget = config.value.ExpBudget
        config.value.Budget = budget - config.value.budget0

        csv_filename, csv_parent_folder = get_filename_and_parent(config.value.file)
        csv_budget = math.ceil(math.sqrt(len(data.rows)))
        stats_dir = f"../results/stats/{csv_parent_folder}/{csv_filename}"
        plots_dir = f"../results/plots/{csv_parent_folder}/{csv_filename}"
        treatment = f"b2_{str(budget)}"
        if budget == csv_budget:
            treatment = f"b2_sqrt"
        os.makedirs(stats_dir, exist_ok=True)
        os.makedirs(plots_dir, exist_ok=True)

        stats = []
        sampled_d2h_history = {}

        trials_to_plot = [0, 4, 9, 14, 19]

        for trial in range(repeats):
            best_d2h, d2h_history = data.smo(
                score=lambda b, r: abs(b**2) / abs(r + sys.float_info.min)
            )
            best_d2h = best_d2h.d2h(data)
            stats.append(best_d2h)

            if trial in trials_to_plot:
                sampled_d2h_history[trial] = d2h_history

        smo_plot_performance(config.value.Budget, sampled_d2h_history).savefig(
            f"{plots_dir}/{treatment}.png"
        )

        with open(f"{stats_dir}/{treatment}.txt", "w") as file:
            file.write(f"{treatment} {' '.join(map(str, stats))}")

    def rand_stats(self):
        data = Data(config.value.file, fun=None, sortD2H=False)
        repeats = 20

        budget = config.value.ExpBudget
        config.value.Budget = budget - config.value.budget0

        csv_filename, csv_parent_folder = get_filename_and_parent(config.value.file)
        csv_budget = math.ceil(math.sqrt(len(data.rows)))
        rand_budget = int(0.9 * len(data.rows))
        stats_dir = f"../results/stats/{csv_parent_folder}/{csv_filename}"
        treatment = f"rand_{str(budget)}"
        if budget == csv_budget:
            treatment = f"rand_sqrt"
        if budget == rand_budget:
            treatment = f"rand_p90"
        os.makedirs(stats_dir, exist_ok=True)

        stats = [
            data.clone(shuffle(data.rows[:budget]), sortD2H=True).rows[0].d2h(data)
            for _ in range(repeats)
        ]
        with open(f"{stats_dir}/{treatment}.txt", "w") as file:
            file.write(f"{treatment} {' '.join(map(str, stats))}")

    def gen_params(self):
        k_range = (1, 5)
        m_range = (1, 5)
        budget0_range = (3, 17)
        Budget_range = (3, 17)

        param_space = []
        for k in range(*k_range):
            for m in range(*m_range):
                for budget0 in range(*budget0_range):
                    for Budget in range(*Budget_range):
                        param_space.append(map(str, [k, m, budget0, Budget]))

        random.shuffle(param_space)
        param_space.insert(0, ["k", "m", "budget0", "Budget"])

        param_csv = ""
        for params in param_space:
            param_csv += f"{','.join(params)}\n"

        if config.value.output is not None and len(config.value.output) > 0:
            os.makedirs(os.path.dirname(config.value.output), exist_ok=True)
            with open(config.value.output, "w") as file:
                file.write(param_csv)

        print(param_csv)


def learn(data, row, my) -> None:
    my.n += 1
    kl = row.cells[data.cols.klass.at]
    if my.n > 10:
        my.tries += 1
        my.acc += 1 if kl == row.likes(my.datas)[0] else 0
    my.datas[kl] = my.datas.get(kl, Data(data.cols.names))  # default value --> new data
    my.datas[kl].add(row, None)


def shuffle(rows):
    random.shuffle(rows)
    return rows


def smo_plot_performance(budget: int, d2h_history: List[float]) -> Figure:
    epochs = range(1, budget + 1)

    # Create a figure with two subplots, arranged side-by-side
    fig, axs = plt.subplots(1, 1, figsize=(5, 5))  # Adjust figsize as needed

    # Plot the first subplot (Best D2H)
    for trial_num in d2h_history.keys():
        axs.plot(epochs, d2h_history[trial_num], label=f"trial {trial_num}")

    axs.legend(title="5/20 Trials")
    axs.set_xlabel("Budget Increment Beyond b0")
    axs.set_ylabel("Best D2H")
    axs.grid(True)
    axs.set_ylim(0, max([x for sublist in d2h_history.values() for x in sublist]) * 1.3)

    plt.tight_layout()  # Adjust subplot spacing

    return fig


def sim_annealing_plot_performance(
    budget: int, d2h_history: List[float], b_exp_values: List[float]
) -> Figure:
    epochs = range(1, budget + 1)

    # Create a figure with two subplots, arranged side-by-side
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # Adjust figsize as needed

    # Plot the first subplot (Best D2H)
    for trial_num in d2h_history.keys():
        axs[0].plot(epochs, d2h_history[trial_num], label=f"trial {trial_num}")

    axs[0].legend(title="5/20 Trials")
    axs[0].set_xlabel("Budget Increment Beyond b0")
    axs[0].set_ylabel("Best D2H")
    axs[0].grid(True)
    axs[0].set_ylim(
        0, max([x for sublist in d2h_history.values() for x in sublist]) * 1.3
    )

    # Plot the second subplot (b Exponent)
    axs[1].scatter(
        epochs,
        b_exp_values,
    )
    axs[1].set_xlabel("Budget Increment Beyond b0")
    axs[1].set_ylabel("b Exponent")
    axs[1].grid(True)

    # axs[0].set_ylim([x - 1 for x in axs[1].get_ylim()])

    # NOTE: No title because we will add it in overleaf
    # Add overall title to the figure
    # fig.suptitle('"Simulated Annealing" Acquisition Performance')

    # plt.subplots_adjust(top=0.70)  # Adjust top spacing for title

    plt.tight_layout()  # Adjust subplot spacing

    return fig


def exp_progressive_plot_performance(
    budget: int, d2h_history: List[float], want_to_exploit: List[float]
) -> Figure:
    epochs = range(1, budget + 1)

    # Create a figure with two subplots, arranged side-by-side
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # Adjust figsize as needed

    # Plot the first subplot (Best D2H)
    for trial_num in d2h_history.keys():
        axs[0].plot(epochs, d2h_history[trial_num], label=f"trial {trial_num}")

    axs[0].legend(title="5/20 Trials")
    axs[0].set_xlabel("Budget Increment Beyond b0")
    axs[0].set_ylabel("Best D2H")
    axs[0].grid(True)
    axs[0].set_ylim(
        0, max([x for sublist in d2h_history.values() for x in sublist]) * 1.3
    )

    # Plot the second subplot (b Exponent)
    axs[1].scatter(epochs, want_to_exploit, label="want to exploit")
    axs[1].scatter(epochs, [1 - x for x in want_to_exploit], label="want to explore")
    axs[1].legend()
    axs[1].set_xlabel("Budget Increment Beyond b0")
    axs[1].grid(True)

    # axs[0].set_ylim([x - 1 for x in axs[1].get_ylim()])

    # NOTE: No title because we will add it in overleaf
    # Add overall title to the figure
    # fig.suptitle('"Simulated Annealing" Acquisition Performance')

    # plt.subplots_adjust(top=0.70)  # Adjust top spacing for title

    plt.tight_layout()  # Adjust subplot spacing

    return fig

import matplotlib.pyplot as plt
import sys


def parse_results_from_output(stats_filename, acquisition_functions):
    acquisition_fn_map = {}
    with open(stats_filename, "r") as file:
        for line in file:
            line_components = line.split(",")
            if (len(line_components) <= 1) or line_components[0] == "rank":
                continue
            line_components = [x.strip() for x in line_components]
            rank, acqn, d2h = line_components[0], line_components[1], line_components[2]
            acquisition_fn, budget = "", ""
            split_acqn = acqn.split("_")
            # If the "treatment" doesn't contain both the acqn fn name and a budget, then skip
            # this iteration
            if len(split_acqn) < 2:
                continue
            acquisition_fn, budget = split_acqn[0], split_acqn[1]

            if acquisition_fn not in acquisition_functions:
                continue

            if acquisition_fn_map.get(acquisition_fn) is None:
                acquisition_fn_map[acquisition_fn] = {}
            acquisition_fn_map[acquisition_fn][budget] = float(d2h)

    return acquisition_fn_map


def sort_budgets(budgets):
    numbers = []
    for budget in budgets:
        if budget.isnumeric():
            numbers.append(int(budget))
    numbers.sort()
    sorted_budgets = [str(x) for x in numbers]
    if "sqrt" in budgets:
        sorted_budgets.append("sqrt")
    return sorted_budgets


def plot_bargraphs(stats, stats_filename, acquisition_functions):
    budgets = list(stats[acquisition_functions[0]].keys())
    budgets = sort_budgets(budgets)
    print("Budgets: ", budgets)
    distances_to_heaven = [
        stats[func][budget] for func in acquisition_functions for budget in budgets
    ]

    max_distance = max(distances_to_heaven)
    y_max = max_distance * 1.3

    # Plotting the bar graph
    plt.figure(figsize=(10, 6))
    colors = ["blue", "orange", "green", "red", "purple"]

    for i, func in enumerate(acquisition_functions):
        plt.bar(
            [(j + 1) + i * 0.15 for j in range(len(budgets))],
            [stats[func][b] for b in budgets],
            width=0.15,
            label=func,
            color=colors[i],
        )

    plt.xlabel("Budgets")
    plt.ylabel("Distances to Heaven")
    plt.title("Bar Graph of Distances to Heaven by Budget and Acquisition Function")
    plt.xticks([1.3 + x for x in range(len(budgets))], budgets)
    plt.ylim(0, y_max)
    plt.legend()
    plt.grid(axis="y")

    destination_filename = (
        "../results/plots/bargraphs/"
        + ("/".join(stats_filename.split("/")[-2:]))[:-3]
        + "png"
    )
    print("Destination filename: ", destination_filename)
    plt.savefig(destination_filename, bbox_inches="tight")


if __name__ == "__main__":
    stats_filename = ""
    acquisition_functions = [
        "progressive",
        "focus",
        "bonr",
        "b2",
        "ExpProgressive",
    ]
    if len(sys.argv) != 2:
        print("Provide the filename of an output file as the command line argument")
    else:
        stats_filename = sys.argv[1]

    stats = parse_results_from_output(stats_filename, acquisition_functions)
    print(stats)
    plot_bargraphs(stats, stats_filename, acquisition_functions)

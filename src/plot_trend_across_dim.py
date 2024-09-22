import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np


def find_lowest_rank_and_budget(filename, target):
    lowest_rank = float("inf")
    lowest_budget = float("inf")
    mean_d2h = None
    std_d2h = None

    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == "#":
                continue
            rank = int(row[0].strip())
            acquisition_function = row[1].strip()
            budget = int(row[2].strip())
            mean = float(row[3].strip())
            std = float(row[4].strip())

            if acquisition_function == target and rank < lowest_rank:
                lowest_rank = rank
                lowest_budget = budget
                mean_d2h = mean
                std_d2h = std
            elif acquisition_function == target and rank == lowest_rank:
                if budget < lowest_budget:
                    lowest_budget = budget
                    mean_d2h = mean
                    std_d2h = std
            elif acquisition_function == target and rank > lowest_rank:
                break

    return lowest_rank, lowest_budget, mean_d2h, std_d2h


def plot_stats_per_dataset(focus_map, rand_map, baseline_map):
    focus_vals = [focus_map[file] for file in sorted_files]
    rand_vals = [rand_map[file] for file in sorted_files]
    baseline_vals = [baseline_map[file] for file in sorted_files]

    # Create x-axis values (file indices)
    x = np.arange(len(sorted_files))

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(x, focus_vals, "b-", label="Focus")
    plt.plot(x, rand_vals, "r-", label="Rand")
    plt.plot(x, baseline_vals, "g-", label="Baseline")
    # plt.plot(x, )

    # Customize the plot
    plt.xlabel("File Index")
    plt.ylabel("Best d2h")
    plt.title("Best d2h for Focus and Rand across Sorted Files")
    plt.legend()

    # Add grid for better readability
    plt.grid(True, linestyle="--", alpha=0.7)

    # Rotate x-axis labels for better visibility
    plt.xticks(x[::5], range(0, len(sorted_files), 5), rotation=45)

    # Adjust layout to prevent clipping of labels
    plt.tight_layout()

    # Show the plot
    plt.show()


def write_stats_to_file(
    filenames, files_to_dim_map, focus_stats, rand_stats, baseline_stats
):
    with open("../results/cat_a_b_stats_summary.csv", "w") as file:
        file.write(
            f"{'Dataset':<50},{'X var count':<25},{'Focus best rank':<25},{'Focus best d2h':<25},{'Focus std':<25},{'Rand best rank':<25},{'Rand best d2h':<25},{'Rand std':<25},"
            f"{'Baseline best rank':<25},{'Baseline best d2h':<25},{'Baseline std':<25}\n"
        )

        for filename in filenames:
            file.write(
                f"{filename:<50}, "
                f"{files_to_dim_map[filename]:<25}"
                f"{focus_stats['best rank'][filename]:<25}, "
                f"{focus_stats['d2h'][filename]:<25}, "
                f"{focus_stats['std'][filename]:<25}, "
                f"{rand_stats['best rank'][filename]:<25}, "
                f"{rand_stats['d2h'][filename]:<25}, "
                f"{rand_stats['std'][filename]:<25}, "
                f"{baseline_stats['best rank'][filename]:<25}, "
                f"{baseline_stats['d2h'][filename]:<25}, "
                f"{baseline_stats['std'][filename]:<25}\n"
            )

    return


if __name__ == "__main__":
    df = pd.read_csv("../results/cat_a_b_summary.csv")
    df["Independent Variables"] = df["Numeric"] + df["Symbolic"]
    sorted_df = df.sort_values(by="Independent Variables")
    sorted_files = sorted_df["File Name"].tolist()
    sorted_ipvar_count = sorted_df["Independent Variables"].tolist()

    files_to_dim_map = {}
    for i in range(len(sorted_files)):
        files_to_dim_map[sorted_files[i]] = sorted_ipvar_count[i]

    focus_dataset_bestd2h_map = {}
    focus_dataset_bestrank_map = {}
    focus_dataset_std_map = {}

    rand_dataset_bestd2h_map = {}
    rand_dataset_bestrank_map = {}
    rand_dataset_std_map = {}

    baseline_dataset_d2h_map = {}
    baseline_dataset_rank_map = {}
    baseline_dataset_std_map = {}

    for filename in sorted_files:
        sk_result_filename = filename.replace(".csv", ".sk.txt")
        sk_result_file_location = "../results/sk/cat_a_b/" + sk_result_filename

        focus_rank, focus_budget, focus_mean, focus_std = find_lowest_rank_and_budget(
            sk_result_file_location, "focus"
        )
        rand_rank, rand_budget, rand_mean, rand_std = find_lowest_rank_and_budget(
            sk_result_file_location, "rand"
        )
        (
            baseline_rank,
            baseline_budget,
            baseline_mean,
            baseline_std,
        ) = find_lowest_rank_and_budget(sk_result_file_location, "baseline")

        focus_dataset_bestd2h_map[filename] = focus_mean
        focus_dataset_bestrank_map[filename] = focus_rank
        focus_dataset_std_map[filename] = focus_std

        rand_dataset_bestd2h_map[filename] = rand_mean
        rand_dataset_bestrank_map[filename] = rand_rank
        rand_dataset_std_map[filename] = rand_std

        baseline_dataset_d2h_map[filename] = baseline_mean
        baseline_dataset_rank_map[filename] = baseline_rank
        baseline_dataset_std_map[filename] = baseline_std

    focus_stats = {
        "best rank": focus_dataset_bestrank_map,
        "d2h": focus_dataset_bestd2h_map,
        "std": focus_dataset_std_map,
    }
    rand_stats = {
        "best rank": rand_dataset_bestrank_map,
        "d2h": rand_dataset_bestd2h_map,
        "std": rand_dataset_std_map,
    }
    baseline_stats = {
        "best rank": baseline_dataset_rank_map,
        "d2h": baseline_dataset_d2h_map,
        "std": baseline_dataset_std_map,
    }

    write_stats_to_file(
        sorted_files, files_to_dim_map, focus_stats, rand_stats, baseline_stats
    )

    plot_stats_per_dataset(
        focus_dataset_bestd2h_map, rand_dataset_bestd2h_map, baseline_dataset_d2h_map
    )
    plot_stats_per_dataset(
        focus_dataset_bestrank_map, rand_dataset_bestrank_map, baseline_dataset_rank_map
    )


print("FOCUS d2h map: ", focus_dataset_bestd2h_map)
print("Rand d2h map: ", rand_dataset_bestd2h_map)

print("FOCUS rank map: ", focus_dataset_bestrank_map)
print("Rand rank map: ", rand_dataset_bestrank_map)

print("Baseline d2h map: ", baseline_dataset_d2h_map)
print("Baseline d2h rank map: ", baseline_dataset_rank_map)

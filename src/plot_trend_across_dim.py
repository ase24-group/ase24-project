import pandas as pd
import csv


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


if __name__ == "__main__":
    df = pd.read_csv("../results/cat_a_b_summary.csv")
    df["Independent Variables"] = df["Numeric"] + df["Symbolic"]
    sorted_df = df.sort_values(by="Independent Variables")
    sorted_files = sorted_df["File Name"].tolist()

    focus_dataset_bestd2h_map = {}
    focus_dataset_bestrank_map = {}

    rand_dataset_bestd2h_map = {}
    rand_dataset_bestrank_map = {}

    baseline_dataset_d2h_map = {}
    baseline_dataset_rank_map = {}

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

        rand_dataset_bestd2h_map[filename] = rand_mean
        rand_dataset_bestrank_map[filename] = rand_rank

        baseline_dataset_d2h_map[filename] = baseline_mean
        baseline_dataset_rank_map[filename] = baseline_rank

print("FOCUS d2h map: ", focus_dataset_bestd2h_map)
print("Rand d2h map: ",  rand_dataset_bestd2h_map)

print("FOCUS rank map: ", focus_dataset_bestrank_map)
print("Rand rank map: ", rand_dataset_bestrank_map)

print("Baseline d2h map: ", baseline_dataset_d2h_map)
print("Baseline d2h rank map: ", baseline_dataset_rank_map)

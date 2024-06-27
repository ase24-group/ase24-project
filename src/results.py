import os
import shutil
import sys
from stats import write_scott_knott_results
from utils import get_filename_and_parent


# Removing the folder whose name is passed as argument
def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)


def combine_stats_files(csv_path):
    combined_file_contents = ""
    csv_filename, csv_parent_folder = get_filename_and_parent(csv_path)
    directory_path = f"../results/stats/{csv_parent_folder}/{csv_filename}"

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as input_file:
                combined_file_contents += f"{input_file.read()}\n\n"

    with open(
        f"../results/stats/{csv_parent_folder}/{csv_filename}.stats.txt", "w"
    ) as output_file:
        output_file.write(combined_file_contents)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify the csv path")
        print('python3 results.py <csv_path>')
        exit(1)

    csv_path = sys.argv[1]
    csv_filename, csv_parent_folder = get_filename_and_parent(csv_path)

    combine_stats_files(csv_path)
    delete_folder(f"../results/stats/{csv_parent_folder}/{csv_filename}")
    write_scott_knott_results(csv_path)

import os
import shutil
import subprocess
import sys
import math
from data import Data
from stats import write_scott_knott_results
from datetime import datetime
from utils import get_filename_and_parent


# Removing the folder whose name is passed as argument
def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)


def generate_makefile(csv_path):
    data = Data(csv_path, fun=None, sortD2H=False)
    csv_filename, csv_parent_folder = get_filename_and_parent(csv_path)

    makefile_arg = (
        "ARGUMENT := -f ../data/auto93.csv\n\nifdef ARG\n\tARGUMENT := $(ARG)\nendif"
    )
    all_targets = []
    targets = {}

    csv_budget = math.ceil(math.sqrt(len(data.rows)))
    rand_budget = int(0.9 * len(data.rows))
    treatments = ["progressive", "SimAnnealing", "bonr", "b2", "rand", "ExpProgressive", "PI", "UCB"]

    id = f"base"
    all_targets.append(id)
    targets[id] = f"python3 gate.py -t base_stats $(ARGUMENT)"
    for treatment in treatments:
        for e in [9, 15, csv_budget]:
            id = f"{treatment}{e}"
            all_targets.append(id)
            targets[id] = f"python3 gate.py -t {treatment}_stats -E {e} $(ARGUMENT)"
    id = f"rand{rand_budget}"
    all_targets.append(id)
    targets[id] = f"python3 gate.py -t rand_stats -E {rand_budget} $(ARGUMENT)"

    makefile_all = f"all: {' '.join(all_targets)}"
    makefile_targets = ""

    for target, command in targets.items():
        makefile_targets += f"{target}:\n\t{command}\n\n"

    makefile = f"{makefile_arg}\n\n{makefile_all}\n\n{makefile_targets}"

    os.makedirs(f"makefiles/{csv_parent_folder}", exist_ok=True)
    with open(f"makefiles/{csv_parent_folder}/{csv_filename}.mk", "w") as file:
        file.write(makefile)


def run_makefile(makefile_arg, csv_path):
    csv_filename, csv_parent_folder = get_filename_and_parent(csv_path)
    makefile_path = f"makefiles/{csv_parent_folder}/{csv_filename}.mk"

    command = ["make", "-f", makefile_path, "-j", "100", "-s", makefile_arg]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Makefile execution failed with return code {e.returncode}.")
        print(e.output.decode())  # Print the error output, if any


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


def find_csv_filename(makefile_arg):
    arg_components = makefile_arg.split()
    i = 0
    if "-f" not in arg_components:
        print("A '-f argument must be passed'")
        exit(1)
    while arg_components[i] != "-f" and i < len(arg_components):
        i += 1

    if i == len(arg_components) - 1:
        print("A file name must be provided after the -f flag")
        exit(1)
    return arg_components[i + 1]


if __name__ == "__main__":
    makefile_arg = ""
    if len(sys.argv) < 2:
        print(
            "Atleast one argument must be provided as a string specifying the arguments for SMO in the format:"
        )
        print('python main.py "-f <filename> -m <m> -k <k>......"')
        exit(1)
    else:
        makefile_arg = "ARG=" + sys.argv[1]

    csv_path = find_csv_filename(makefile_arg[4:])
    csv_filename, csv_parent_folder = get_filename_and_parent(csv_path)

    delete_folder(f"../results/stats/{csv_parent_folder}/{csv_filename}")
    generate_makefile(csv_path)
    run_makefile(makefile_arg, csv_path)
    combine_stats_files(csv_path)
    delete_folder(f"../results/stats/{csv_parent_folder}/{csv_filename}")
    write_scott_knott_results(csv_path)

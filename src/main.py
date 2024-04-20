import os
import shutil
import subprocess
import sys
import math
from data import Data
from stats import egSlurp, slurp, Sample, sk
from datetime import datetime


# Removing the contents of the folder whose name is passed as argument
def delete_folder_contents(folder_path):
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    else:
        print(f"Folder '{folder_path}' does not exist.")


def generate_makefile(csv_filename):
    data = Data(csv_filename, fun=None, sortD2H=False)

    makefile_arg = "ARGUMENT := -f ../data/auto93.csv\n\nifdef ARG\n\tARGUMENT := $(ARG)\nendif"
    all_targets = []
    targets = {}

    csv_budget = math.ceil(math.sqrt(len(data.rows)))
    rand_budget = int(0.9 * len(data.rows))
    treatments = ["progressive", "SimAnnealing", "bonr", "rand", "ExpProgressive"]

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

    with open(f"Makefile", "w") as file:
        file.write(makefile)


def run_makefile(makefile_arg):
    command = ["make", "-j", "100", "-s", makefile_arg]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Makefile execution failed with return code {e.returncode}.")
        print(e.output.decode())  # Print the error output, if any


def combine_stats_files(directory_path):
    combined_file_contents = ""
    files_to_remove = []

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as input_file:
                combined_file_contents += input_file.read() + "\n\n"
                files_to_remove.append(file_path)
                # output_file.write(file_contents)
    for file_path in files_to_remove:
        os.remove(file_path)

    with open(directory_path + "/stats.txt", "w") as output_file:
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


# Takes in all the SMO results from an input file and ranks them based on Scott-Knott
# to an output file
def write_scott_knott_results(input_file, csv_file):
    output_file = "../output" + csv_file[7:]
    # Emptying the file first
    with open(output_file, "w") as file:
        pass
    with open(output_file, "a") as file:
        file.write(f'date    : {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}' + "\n")
        file.write(f"file    : {csv_filename}" + "\n\n")
        nums = slurp(input_file)
        all = Sample([x for num in nums for x in num.has])
        last = None
        for num in sk(nums):
            if num.rank != last:
                file.write("#\n")
            last = num.rank
            file.write(all.bar(num, width=40, word="%20s", fmt="%5.2f")+"\n")
    

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

    csv_filename = find_csv_filename(makefile_arg[4:])

    delete_folder_contents("./stats")
    generate_makefile(csv_filename)
    run_makefile(makefile_arg)
    combine_stats_files("./stats")
    # egSlurp("./stats/stats.txt")
    write_scott_knott_results("./stats/stats.txt", csv_filename)

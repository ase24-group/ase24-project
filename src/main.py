import os
import shutil
import subprocess
import sys
from stats import egSlurp


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


def run_makefile(makefile_path, makefile_arg):
    command = ["make", "-j", 10, makefile_arg]
    try:
        subprocess.run(command, check=True)
        print("Makefile executed successfully.")
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
                combined_file_contents += "\n" + input_file.read()
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
    while arg_components[i] is not "-f":
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

    csv_filename = find_csv_filename(makefile_arg[4:])

    delete_folder_contents("./stats")
    run_makefile("Makefile", makefile_arg)
    combine_stats_files("./stats")
    egSlurp("./stats/stats.txt", csv_filename)

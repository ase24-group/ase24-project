import os
import shutil


dim_levels = ["low", "medium", "high"]

# Create the target directory if it doesn't exist
os.makedirs("../results/sk/cat_a_b/dim_split/low", exist_ok=True)
os.makedirs("../results/sk/cat_a_b/dim_split/medium", exist_ok=True)
os.makedirs("../results/sk/cat_a_b/dim_split/high", exist_ok=True)



# Read the filenames from the source file
for dim_level in dim_levels:
    with open("../results/sk/cat_a_b/dim_split/"+dim_level+".txt", 'r') as file:
        filenames = file.read().splitlines()
    # Copy each file to the target directory
    for filename in filenames:
        filename = "../results/sk/cat_a_b/"+filename
        if os.path.isfile(filename):
            shutil.copy(filename, "../results/sk/cat_a_b/dim_split/"+dim_level+"/")
            print(f'Copied: {filename}')
        else:
            print(f'File not found: {filename}')
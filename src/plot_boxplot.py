import matplotlib.pyplot as plot
import os
from utils import get_filename_and_parent

stats_file = '../results/stats/flash/ranks.stats.txt'
_, parent_folder = get_filename_and_parent(stats_file)

# Read data from file
with open(stats_file, 'r') as file:
    lines = file.readlines()

# Parse data
data = {}
for line in lines:
    parts = line.split()
    treatment = parts[0]
    values = list(map(int, parts[1:]))
    data[treatment] = values

# Function to calculate the median without numpy
def calculate_median(data):
    sorted_data = sorted(data)
    length = len(sorted_data)
    if length % 2 == 0:
        return (sorted_data[length // 2 - 1] + sorted_data[length // 2]) / 2
    else:
        return sorted_data[length // 2]

# Calculate median values for each treatment
medians = {treatment: calculate_median(values) for treatment, values in data.items()}

# Sort treatments based on median values
sorted_treatments = sorted(data.keys(), key=lambda x: -medians[x])

# Define colors based on treatment names
colors = {'SimAnnealing': 'salmon', 'progressive': 'olivedrab', 'ExpProgressive': 'dodgerblue'}

# Create a box plot for sorted treatments
box = plot.boxplot([data[treatment] for treatment in sorted_treatments], vert=False, patch_artist=True, medianprops=dict(color='goldenrod', linewidth=2))

# Add title and labels
plot.title('Box Plot for Treatments')
plot.ylabel('Treatments')
plot.xlabel('Ranks')

# Add treatment labels to y-axis
plot.yticks(range(1, len(sorted_treatments) + 1), sorted_treatments)

for tick_label in plot.gca().get_yticklabels():
    if tick_label.get_text().split("_")[0] in colors:
        tick_label.set_color(colors.get(tick_label.get_text().split("_")[0], 'black'))

# Customize box colors
for patch, treatment in zip(box['boxes'], sorted_treatments):
    patch.set_facecolor(colors.get(treatment.split("_")[0], 'white'))

plots_dir = f"../results/plots/boxplots/{parent_folder}"
os.makedirs(plots_dir, exist_ok=True)

# Save the plot to a file
plot.savefig(f"{plots_dir}/ranks.boxplot.png", bbox_inches='tight')

# Close the plot to release resources
plot.close()

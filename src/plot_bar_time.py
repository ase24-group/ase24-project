import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

# Read the CSV file
filename = "../results/times/cat_a_b.times.csv"
data = defaultdict(lambda: defaultdict(list))

with open(filename, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["treatment"] != "baseline":
            budget = int(row["budget"])
            treatment = row["treatment"]
            time = float(row["time"])
            data[treatment][budget].append(time)

# Calculate the median time for each treatment at each budget
medians = {
    treatment: {budget: np.median(times) for budget, times in budgets.items()}
    for treatment, budgets in data.items()
}

# Create the plot
budgets = sorted(
    set(budget for treatment_budgets in data.values() for budget in treatment_budgets)
)
treatments = sorted(medians.keys())
bar_width = 0.1

fig, ax = plt.subplots(figsize=(12, 6))

for i, treatment in enumerate(treatments):
    treatment_medians = [medians[treatment].get(budget, 0) for budget in budgets]
    positions = [j + i * bar_width for j in range(len(budgets))]
    ax.bar(positions, treatment_medians, bar_width, label=treatment)

# Set the position of the x ticks
ax.set_xticks([j + bar_width * (len(treatments) - 1) / 2 for j in range(len(budgets))])
ax.set_xticklabels(budgets)

ax.set_xlabel("Budget")
ax.set_ylabel("Median Time")
ax.set_title("Median Time by Budget for Different Treatments")
ax.legend(title="Treatment")
ax.grid(True, axis="y")

plt.show()

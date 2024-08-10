import csv
import matplotlib.pyplot as plt
from collections import defaultdict

# Read the CSV file
filename = '../results/times/cat_a_b.times.csv'
data = defaultdict(lambda: defaultdict(list))

with open(filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if(row['treatment'] != 'baseline'):
            budget = int(row['budget'])
            treatment = row['treatment']
            time = float(row['time'])
            data[treatment][budget].append(time)

# Calculate the average time for each treatment at each budget
averages = {treatment: {budget: sum(times)/len(times) for budget, times in budgets.items()} for treatment, budgets in data.items()}

# Plotting
plt.figure(figsize=(10, 6))
for treatment, budgets in averages.items():
    budgets_sorted = sorted(budgets.items())
    budgets, times = zip(*budgets_sorted)
    if (treatment == 'bonr'):
        treatment = 'uncertain';
    if (treatment == 'b2'):
        treatment = 'certain';
    plt.plot(budgets, times, marker='o', label=treatment)

plt.xlabel('Budget')
plt.ylabel('Average Time')
plt.title('Average time by budget for different treatments')
plt.legend(title='Treatment')
plt.grid(True)
plt.show()
# plt.savefig(f"cat_a_b.times.png", bbox_inches="tight")

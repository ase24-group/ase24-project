import os
import csv

folder_path = '../data/cat_a_b'
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
data_info = []

for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    Xs = 0
    Ys = 0
    maxs = 0
    mins = 0
    nums = 0
    syms = 0

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for column in columns:
            column = column.strip()
            if column[-1] != "X":
                if column[-1] == "+":
                    maxs += 1
                elif column[-1] == "-":
                    mins += 1
                elif column[0].isupper():
                    nums += 1 
                elif column[0].islower():
                    syms += 1

        num_columns = len(columns)
        num_rows = sum(1 for row in reader)
        
    
    data_info.append([csv_file, num_rows, num_columns, nums, syms, maxs, mins])

output_file = '../results/cat_a_b_summary.csv'
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['File Name', 'Number of Rows', 'Number of Columns', "Numeric", "Symbolic", "Maximize", "Minimize"])
    writer.writerows(data_info)

print(f'Summary has been written to {output_file}')
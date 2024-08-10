import csv

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    return data

def normalize_data(data):
    values = [[int(cell) for cell in row[1:]] for row in data[1:]]
    max_value = max(max(row) for row in values)
    # normalized = [[cell / max_value for cell in row] for row in values]
    normalized = [[(cell - custom_min) / (max_value - custom_min) if cell > custom_min else 0 for cell in row] for row in values]
    return normalized, max_value

def color_cell(red_value, value):
    if int(value) == 0:
        return ""
    red_intensity = red_value * 100
    if red_intensity >= 50:
        return f"\\cellcolor{{red!{int(red_intensity)}}}\\textcolor{{white}}{{{int(value)}}}"
    else:
        return f"\\cellcolor{{red!{int(red_intensity)}}}{int(value)}"

def generate_latex_table(data, normalized, max_value):
    header = data[0]
    rows = data[1:]

    latex_code = "\\begin{tabular}{r|" + "c" * (len(header) - 1) + "}\n"
    latex_code += "Rank & " + " & ".join(header[1:]) + " \\\\\n"
    latex_code += "\\hline\n"

    for i, row in enumerate(rows):
        latex_code += row[0]
        for j, val in enumerate(normalized[i]):
            latex_code += f" & {color_cell(val, data[i + 1][j + 1])}"
        latex_code += " \\\\\n"

    latex_code += "\\end{tabular}"
    return latex_code

# Read the CSV data
file_path = '../results/sk/cat_a_b/dim_split/high/rq_high.budget.csv'
data = read_csv(file_path)

custom_min = 35
# Normalize the data
normalized, max_value = normalize_data(data)

# Generate the LaTeX table
latex_table = generate_latex_table(data, normalized, max_value)

print(latex_table)

# # Save the LaTeX code to a file
# with open("colored_table.tex", "w") as f:
#     f.write(latex_table)

# print("LaTeX table generated successfully!")

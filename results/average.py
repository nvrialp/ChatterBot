import csv

filename = 'kris.csv'
adequacy = 'Adequacy'
sense = 'Sense'

with open(filename, newline='') as csvfile:
    reader = list(csv.reader(csvfile))  # Convert to list so we can iterate multiple times
    header = reader[0]
    data = reader[1:]

    for column in [adequacy, sense]:
        if column not in header:
            print("Column not found:", column)
        else:
            index = header.index(column)
            total = 0.0
            count = 0

            for row in data:
                try:
                    value = float(row[index])
                    total += value
                    count += 1
                except (ValueError, IndexError):
                    pass  # Skip missing or non-numeric values

            if count > 0:
                average = total / count
                print(f"Average of '{column}':", average)
            else:
                print(f"No numeric data found in column '{column}'")
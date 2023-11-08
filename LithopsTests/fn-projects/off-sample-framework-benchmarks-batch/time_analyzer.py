import csv
import itertools
import json
import os
import numpy as np
import pandas as pd
import ast

directory_path = 'batch_benchmarks/time_results_5_9_23_eu-west/warm'
results=[]
for entry in os.scandir(directory_path):
    if entry.is_file():
        print("File:", entry.name)
    elif entry.is_dir():
        print("Subdirectory:", entry.path)
        list_time_total=[]
        list_time_download=[]
        list_time_inference=[]
        list_time_sum = []
        for subentry in os.scandir(entry.path):
            if subentry.is_file():
                print("File:", subentry.name)
                with open(subentry.path, 'r') as file:
                    times = json.load(file)
                    list_time_total.append(times["invocation_times"])
                    list_time_download.append(times["time_download"])
                    list_time_inference.append(times["time_inference"])
                    list_time_sum.append(times["time_download"]+times["time_inference"])
        print(list_time_total)
        total_times = np.add(list_time_inference,list_time_download)
        parts = entry.name.split("_")
        results.append({
            "dataset": parts[0],
            "batch_size": int(parts[-1]),
            "durations":list_time_sum,
            # "invocation_time_mean": np.mean(list_time_total),
            # "invocation_time_std": np.std(list_time_total),
            "time_download_mean": np.mean(list_time_download),
            "time_download_std": np.std(list_time_download),
            "time_inference_mean": np.mean(list_time_inference),
            "time_inference_std": np.std(list_time_inference),
            "total_time": np.mean(total_times),
            "total_std": np.std(total_times)
        })


results = sorted(results, key=lambda x: (x["dataset"], x['batch_size']))
print(results)
with open("batch_benchmarks/time_results_5_9_23_eu-west.json", "w") as file:
    json.dump(results,file,indent=6)

fieldnames = results[0].keys()
file_path = "batch_benchmarks/time_results_5_9_23_eu-west.csv"
with open(file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Write the column headers
    writer.writerows(results)  # Write the actual data

print("OUTLAYERS")
data = pd.read_csv(file_path)
grouped_data = data.groupby(['dataset', 'batch_size'])
grouped_data_durations = grouped_data['durations']
# Function to calculate outliers based on IQR
def find_outliers_iqr(group):
    values =  ast.literal_eval(group.values[0])
    sorted_data = sorted(values)

    # Step 2: Calculate Q1 and Q3
    n = len(sorted_data)
    q1_index = int(0.25 * (n + 1))  # Index of the first quartile
    q3_index = int(0.75 * (n + 1))  # Index of the third quartile
    q1 = sorted_data[q1_index - 1]  # Q1 value (1-based index)
    q3 = sorted_data[q3_index - 1]  # Q3 value (1-based index)

    # Step 3: Calculate the IQR
    iqr = q3 - q1

    # Step 4: Define lower and upper bounds for outlier detection
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Step 5: Find outliers
    outliers = [x for x in values if x < lower_bound or x > upper_bound]

    return outliers

# Find outliers for each group
outliers = grouped_data_durations.apply(find_outliers_iqr)

# Display the outliers
print(outliers)
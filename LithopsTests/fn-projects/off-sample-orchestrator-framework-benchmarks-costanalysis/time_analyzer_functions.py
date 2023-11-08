import csv
import itertools
import json
import os
import numpy as np
import pandas as pd
import numpy as np
from scipy import stats

directory_path = 'functions_benchmarks_3008/time_results_3_8_23'
results=[]
for entry in os.scandir(directory_path):
    if entry.is_file():
        print("File:", entry.name)
    elif entry.is_dir():
        print("Subdirectory:", entry.path)
        durations=[]
        for subentry in os.scandir(entry.path):
            if subentry.is_file():
                print("File:", subentry.name)
                with open(subentry.path, 'r') as file:
                    times = json.load(file)
                    start_times = times["start"]
                    end_times = times["end"]
                    first_start = min(start_times)
                    last_end = max(end_times)
                    duration = last_end-first_start-5
                    durations.append(duration)
        mean_value = np.mean(durations)
        std_deviation = np.std(durations)
        print(durations)
        parts = entry.name.split("_")

        results.append({
            "state": parts[0],
            "functions": int(parts[-1]),
            "durations":durations,
            "mean": mean_value,
            "std": std_deviation
        })


results = sorted(results, key=lambda x: (x["state"], x["functions"]))
print(results)
with open("functions_benchmarks_3008/time_results_3_8_23.json", "w") as file:
    json.dump(results,file,indent=6)

pairs=[]
for result in results:
    for duration in result["durations"]:
        pair = {"state":result["state"],"functions":result["functions"], "durations":duration}
        pairs.append(pair)

fieldnames = pairs[0].keys()
file_path = "functions_benchmarks_3008/time_results_3_8_23.csv"
with open(file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Write the column headers
    writer.writerows(pairs)  # Write the actual data

print("OUTLAYERS")
data = pd.read_csv(file_path)
grouped_data = data.groupby(['state', 'functions'])['durations']

# Function to calculate outliers based on IQR
def find_outliers_iqr(group):
    q1 = group.quantile(0.25)
    q3 = group.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return group[(group < lower_bound) | (group > upper_bound)]

# Find outliers for each group
outliers = grouped_data.apply(find_outliers_iqr)

# Display the outliers
print(outliers)



groups = [list(v) for l,v in itertools.groupby(pairs, lambda x: (x["state"], x["functions"]))]
outliers = []
for group in groups:
    durations=[]
    for duration in group:
        durations.append(duration["durations"])
    data=np.array(durations)
    mean = np.mean(data)
    std_dev = np.std(data)
    # More than 3 standard deviations from the mean an outlier
    threshold = 3
    # create the condition to find outliers
    outlier = data[np.abs(data - mean) > threshold * std_dev]
    outliers.append(outlier)
print(outliers)


# groups = [list(v) for l,v in itertools.groupby(pairs, lambda x: (x["state"], x["functions"]))]
# outliers = []
# for group in groups:
#     durations=[]
#     for duration in group:
#         durations.append(duration["durations"])
#     data = np.array(durations)
#     #appy the z-score method and lets get the absolute values
#     z_scores = np.abs(stats.zscore(data))
#     # lest using a threshold of 1.96 because this 95% of the data threshold
#     threshold = 1.96
#     outliers = data[z_scores > threshold]
#     print(f"{group[0]['state']} {group[0]['functions']} ,{outliers}")

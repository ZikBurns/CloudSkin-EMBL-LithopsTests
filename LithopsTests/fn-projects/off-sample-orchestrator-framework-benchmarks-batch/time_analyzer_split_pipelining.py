import csv
import json
import os
import numpy as np
import pandas as pd
import ast

directory_path = 'streaming_benchmarks/python311/time_results_02_10_23_parallel_split_pipelining_threadpool/percentile_90'
results=[]
for entry_batch_size in os.scandir(directory_path):
    if entry_batch_size.is_file():
        print("File:", entry_batch_size.name)
    elif entry_batch_size.is_dir():
        print("Subdirectory batch size:", entry_batch_size.path)

        for entry_download_stream_size in os.scandir(entry_batch_size.path):
            if entry_download_stream_size.is_file():
                print("File:", entry_download_stream_size.name)
            elif entry_download_stream_size.is_dir():
                print("Subdirectory stream size:", entry_download_stream_size.path)
                for entry_inference_stream_size in os.scandir(entry_download_stream_size.path):
                    list_time_total = []
                    failed_executions = 0
                    for subentry in os.scandir(entry_inference_stream_size.path):
                        if subentry.is_file():
                            print("File:", subentry.name)
                            with open(subentry.path, 'r') as file:
                                times = json.load(file)
                                if "total_time" in times:
                                    list_time_total.append(times["total_time"])
                                else:
                                    failed_executions = failed_executions + 1
                    splitted=entry_batch_size.name.rsplit("_",1)[1]
                    results.append({
                        "dataset": "percentile_90",
                        "durations": list_time_total,
                        "batch_size": entry_batch_size.name.rsplit("_",1)[1],
                        "download_stream_size": entry_download_stream_size.name.rsplit("_",1)[1],
                        "inference_stream_size": entry_inference_stream_size.name.rsplit("_",1)[1],
                        "total_time": np.mean(list_time_total),
                        "total_std": np.std(list_time_total),
                        "failed_executions": failed_executions
                    })


results = sorted(results, key=lambda x: (x["dataset"], x['batch_size'], x['download_stream_size'], x['inference_stream_size']))
print(results)
with open("streaming_benchmarks/python311/time_results_02_10_23_parallel_split_pipelining_threadpool.json", "w") as file:
    json.dump(results,file,indent=6)

fieldnames = results[0].keys()
file_path = "streaming_benchmarks/python311/time_results_02_10_23_parallel_split_pipelining_threadpool.csv"
with open(file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Write the column headers
    writer.writerows(results)  # Write the actual data

print("OUTLAYERS")
data = pd.read_csv(file_path)
grouped_data = data.groupby(['dataset', 'batch_size', 'download_stream_size', 'inference_stream_size'])
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
import json
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from lithops.serve.serve import LithopsServe

def calc_average(times_dict):
    sum_times = 0
    for start, end in zip(times_dict["start"], times_dict["end"]):
        sum_times += (end - start)
    average = sum_times / len(times_dict["start"])
    return average

def calc_durations(times_dict):
    sum_times = []
    for start, end in zip(times_dict["start"], times_dict["end"]):
        sum_times.append(end - start)
    return sum_times
def histogram(data, file_name):
    start_time_offset = data['start'][0]
    timestamps = [(t - start_time_offset) for t in (data['start'] + data['end'])]
    function_numbers = list(range(len(data['start']))) * 2

    fig, ax = plt.subplots(figsize=(10, 6))

    lines = []
    for i, time in enumerate(data['start']):
        start_time = [time - start_time_offset, function_numbers[i]]
        end_time = [data['end'][i] - start_time_offset, function_numbers[i]]
        line_segment = Line2D([start_time[0], end_time[0]], [start_time[1], end_time[1]], color='gray', alpha=0.6)
        ax.add_line(line_segment)
        lines.append(line_segment)

    ax.plot(timestamps, function_numbers, color='None')

    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Function Number')
    ax.set_title('Histogram Plot')
    ax.legend()

    plt.savefig(file_name)


if __name__ == '__main__':
    with open('datasets/smallest_image.csv') as f:
        urls = f.read().splitlines()
    urls.pop(0)
    num_experiments=1
    index = 0
    num_functions = 50
    urls = urls[0:num_functions]
    payload_body = {
        "chunk_size": 1,
        "images": urls
    }

    server = LithopsServe(clean=False)

    for index in range(num_experiments):
        result = server.run_orchestrator(payload_body, force_cold=True)
        cold_times = json.loads(result["times"])
        cold_durations = calc_durations(cold_times)
        mean_value = np.mean(cold_durations)
        std_deviation = np.std(cold_durations)
        print(f"Mean: {mean_value} - Std: {std_deviation}")

        result = server.run_orchestrator(payload_body)
        warm_times = json.loads(result["times"])
        warm_durations=calc_durations(warm_times)
        mean_value = np.mean(warm_durations)
        std_deviation = np.std(warm_durations)
        print(f"Mean: {mean_value} - Std: {std_deviation}")






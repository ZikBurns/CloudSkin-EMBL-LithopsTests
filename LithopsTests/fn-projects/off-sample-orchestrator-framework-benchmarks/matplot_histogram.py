import json
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
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


filename = f"benchmarks_3008/time_results_3_8_23_model_load_included/cold_900/1.json"
f = open(filename)

loaded_json = json.load(f)


filename=f"matplot_18_10_23/time_results_3_8_23_model_load_included/cold_900/2.png"
os.makedirs(os.path.dirname(filename), exist_ok=True)
histogram(loaded_json, filename)
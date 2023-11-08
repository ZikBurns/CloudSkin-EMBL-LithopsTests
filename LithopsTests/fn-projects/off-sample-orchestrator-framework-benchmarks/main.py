import json
import os

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from lithops.serve.serve import LithopsServe

def calc_average(times_dict):
    sum_times = 0
    for start, end in zip(times_dict["start"], times_dict["end"]):
        sum_times += (end - start)
    average = sum_times / len(times_dict["start"])
    return average

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
    with open('datasets/2016-09-21_16h06m49s__6.csv') as f:
        urls_general = f.read().splitlines()
    urls_general.pop(0)
    num_experiments=1
    # num_functions = [900 ,800, 700, 600, 500, 400, 300, 200, 100, 50]
    num_functions = [5]

    for num_function in num_functions:
        urls = urls_general[0:num_function]
        payload_body = {
            "chunk_size": 1,
            "images": urls
        }

        server = LithopsServe(clean=False)

        for index in range(0, num_experiments):
            result = server.run_orchestrator(payload_body, force_cold=True)
            bodies = json.loads(result["body"])
            time_model_inits = []
            for body in bodies:
                time_model_inits.append(body["time_model_init"])
            cold_times = result["invocation_times"]
            cold_times["time_model_init"] = time_model_inits
            # print(calc_average(warm_times))
            filename = f"benchmarks_3008/time_results_5_9_23/cold_{num_function}/{index}.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            out_file = open(filename, "w")
            json.dump(cold_times, out_file, indent=6)
            out_file.close()
            # filename= f"matplot_25_7_23/cold_{num_function}/{index}.png"
            # os.makedirs(os.path.dirname(filename), exist_ok=True)
            # histogram(cold_times, filename)

        for index in range(0, num_experiments):
            result = server.run_orchestrator(payload_body)
            bodies = json.loads(result["body"])
            time_model_inits = []
            for body in bodies:
                time_model_inits.append(body["time_model_init"])
            warm_times = result["invocation_times"]
            warm_times["time_model_init"] = time_model_inits
            print(calc_average(warm_times))
            filename = f"benchmarks_3008/time_results_5_9_23/warm_{num_function}/{index}.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            out_file = open(filename, "w")
            json.dump(warm_times, out_file, indent=6)
            out_file.close()
            # filename=f"matplot_18_7_23/warm_{num_function}/{index}.png"
            # os.makedirs(os.path.dirname(filename), exist_ok=True)
            # histogram(warm_times, f"matplot/warm_{num_function}/{index}.png")




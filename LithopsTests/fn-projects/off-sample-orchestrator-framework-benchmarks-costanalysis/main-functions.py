import json
import os

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from lithops.serve.serve import LithopsServe


if __name__ == '__main__':
    with open('csvs/1x1.csv') as f:
        urls_general = f.read().splitlines()
    urls_general.pop(0)
    num_experiments=1
    # num_functions = [900 ,800, 700, 600, 500, 400, 300, 200, 100, 50]
    num_functions = [2]

    for num_function in num_functions:
        urls = urls_general[0:num_function]
        payload_body = {
            "chunk_size": 1,
            "images": urls
        }

        server = LithopsServe(clean=False)

        for index in range(0,num_experiments):
            result = server.run_orchestrator(payload_body, force_cold=True)
            cold_times = result["invocation_times"]
            filename = f"functions_benchmarks/time_results_3_8_23/cold_{num_function}/{index}.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            out_file = open(filename, "w")
            json.dump(cold_times, out_file, indent=6)
            out_file.close()

        for index in range(0, num_experiments):
            result = server.run_orchestrator(payload_body)
            warm_times = result["invocation_times"]
            filename = f"functions_benchmarks/time_results_3_8_23/warm_{num_function}/{index}.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            out_file = open(filename, "w")
            json.dump(warm_times, out_file, indent=6)
            out_file.close()



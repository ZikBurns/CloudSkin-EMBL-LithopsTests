import json
import os
from lithops.serve.serve import LithopsServe


if __name__ == '__main__':

    num_experiments=50
    batch_sizes = [1]

    directory_path='csvs'
    for entry in os.scandir(directory_path):
        if entry.is_file():
            filename_without_extension = entry.name[:-4]
            print("Analysing:", filename_without_extension)
            with open(entry.path) as f:
                urls_general = f.read().splitlines()
            urls_general.pop(0)
            for batch_size in batch_sizes:
                urls = urls_general[0:batch_size]
                payload_body = {
                    "chunk_size": batch_size,
                    "images": urls
                }

                server = LithopsServe(clean=False)

                for index in range(0, num_experiments):
                    result = server.run_orchestrator(payload_body, force_cold=True)
                    result_body = json.loads(result["body"])
                    result_body = result_body[0]["body"]
                    time_download = result_body['time_download']
                    time_inference = result_body['time_inference']
                    time_model_init = result_body['time_model_init']
                    start_times = result['invocation_times']['start']
                    end_times = result['invocation_times']['end']
                    first_start = min(start_times)
                    last_end = max(end_times)
                    predictions = result_body['predictions']
                    benchmark_result = {'invocation_times': result['invocation_times'],
                                        'invocation_time': last_end - first_start,
                                        'time_model_init':time_model_init,'time_download': time_download,
                                        'time_inference': time_inference, 'predictions': predictions}
                    filename = f"batch_benchmarks_7077/time_results_2_8_23_time_model_init/cold/{filename_without_extension}_{batch_size:03d}/{index}.json"
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    out_file = open(filename, "w")
                    json.dump(benchmark_result, out_file, indent=6)
                    out_file.close()

                for index in range(0, num_experiments):
                    result = server.run_orchestrator(payload_body)
                    result_body = json.loads(result["body"])[0]["body"]
                    time_download=result_body['time_download']
                    time_inference=result_body['time_inference']
                    time_model_init = result_body['time_model_init']
                    start_times = result['invocation_times']['start']
                    end_times = result['invocation_times']['end']
                    first_start = min(start_times)
                    last_end = max(end_times)
                    predictions = result_body['predictions']
                    benchmark_result = {'invocation_times': result['invocation_times'],
                                        'invocation_time': last_end - first_start,
                                        'time_model_init': time_model_init, 'time_download': time_download,
                                        'time_inference': time_inference, 'predictions': predictions}
                    filename = f"batch_benchmarks_7077/time_results_2_8_23_time_model_init/warm/{filename_without_extension}_{batch_size:03d}/{index}.json"
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    out_file = open(filename, "w")
                    json.dump(benchmark_result, out_file, indent=6)
                    out_file.close()





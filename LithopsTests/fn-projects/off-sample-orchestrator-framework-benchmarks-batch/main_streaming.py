import json
import os
from lithops.serve.serve import LithopsServe


if __name__ == '__main__':
    num_experiments=200
    stream_sizes = [16]
    batch_sizes = [32]
    directory_path='csvs'
    for entry in os.scandir(directory_path):
        if entry.is_file():
            filename_without_extension = entry.name[:-4]
            print("Analysing:", filename_without_extension)
            with open(entry.path) as f:
                urls_general = f.read().splitlines()
            urls_general.pop(0)
            for batch_size in batch_sizes:
                urls_general=urls_general*2
                urls = urls_general[0:batch_size]
                for stream_size in stream_sizes:
                    payload_body = {
                        "chunk_size": batch_size,
                        "stream_size":stream_size,
                        "images": urls
                    }
                    server = LithopsServe(clean=False)
                    for index in range(50, num_experiments):
                        result = server.run_orchestrator(payload_body, force_cold=False)
                        print(result)
                        result_body = json.loads( result["body"] )
                        print(result_body)
                        benchmark_result=result_body
                        filename = f"streaming_benchmarks/time_results_15_9_23_threading/{filename_without_extension}/batch_size_{batch_size:03d}/stream_size_{stream_size:03d}/{index}.json"
                        os.makedirs(os.path.dirname(filename), exist_ok=True)
                        out_file = open(filename, "w")
                        json.dump(benchmark_result, out_file, indent=6)
                        out_file.close()






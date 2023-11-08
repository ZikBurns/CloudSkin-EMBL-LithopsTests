import json
import os
from lithops.serve.serve import LithopsServe


if __name__ == '__main__':
    num_experiments=1
    download_stream_sizes = [1]
    inference_stream_sizes = [8]
    batch_sizes = [32]
    directory_path='csvs'
    for entry in os.scandir(directory_path):
        if entry.is_file():
            filename_without_extension = entry.name[:-4]
            print("Analysing:", filename_without_extension)
            with open(entry.path) as f:
                urls_general = f.read().splitlines()
            urls_general.pop(0)
            server = LithopsServe(clean=False)
            for batch_size in batch_sizes:
                urls_general=urls_general*2
                urls = urls_general[0:batch_size]
                for download_stream_size in download_stream_sizes:
                    for inference_stream_size in inference_stream_sizes:
                        payload_body = {
                            "chunk_size": batch_size,
                            "stream_size": inference_stream_size,
                            "download_stream_size":download_stream_size,
                            "inference_stream_size":inference_stream_size,
                            "images": urls
                        }
                        for index in range(0, num_experiments):
                            result = server.run_orchestrator(payload_body, force_cold=False)
                            result_body = json.loads(result["body"])
                            print(result_body)
                            benchmark_result=result_body
                            filename = f"streaming_benchmarks/time_results_19_9_23_split_pipelining/{filename_without_extension}/batch_size_{batch_size:03d}/download_stream_size_{download_stream_size:03d}/inference_stream_size_{inference_stream_size:03d}/{index}.json"
                            os.makedirs(os.path.dirname(filename), exist_ok=True)
                            out_file = open(filename, "w")
                            json.dump(benchmark_result, out_file, indent=6)
                            out_file.close()






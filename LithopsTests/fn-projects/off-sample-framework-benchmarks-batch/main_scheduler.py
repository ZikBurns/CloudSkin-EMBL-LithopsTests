import os
import platform
from lithops import FunctionExecutor


if __name__ == '__main__':
    directory_path='csvs'
    split_size = 1
    num_functions = 1

    for entry in os.scandir(directory_path):
        if entry.is_file():
            filename_without_extension = entry.name[:-4]
            print("Analysing:", filename_without_extension)
            with open(entry.path) as f:
                urls_general = f.read().splitlines()
            urls_general.pop(0)
            urls_general = urls_general[0:split_size]
            urls_general=urls_general*num_functions
            splits = [urls_general[i:i + split_size] for i in range(0, len(urls_general), split_size)]
            fexec = FunctionExecutor(reset=False, runtime_memory=3008)
            payload_list = []
            for split in splits:
                payload_list.append({'payload': {'body':
                    {
                        'images': split,
                        'grpc_port': 50051,
                        'config' : {
                            'load': {'batch_size': 0, 'max_concurrency': 0},
                            'predict': {'interop': 0, 'intraop': 0, 'n_models': 0},
                            'preprocess': {'batch_size': 0, 'intraop': 0, 'num_cpus': 0}
                    }
                }}})
            results, invocation_times = fexec.map_cnn_threading_benchmark(payload_list, force_cold=False)
            preds = []
            for res in results:
                body = res['body']
                preds.append(body['predictions'])
            print(results)
            fexec.close()






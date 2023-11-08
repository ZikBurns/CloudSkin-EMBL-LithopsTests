import os
import platform

from lithops import FunctionExecutor


if __name__ == '__main__':
    directory_path='csvs'
    pyversion_tuple=platform.python_version_tuple()
    hola = pyversion_tuple[0]+pyversion_tuple[1]
    for entry in os.scandir(directory_path):
        if entry.is_file():
            filename_without_extension = entry.name[:-4]
            print("Analysing:", filename_without_extension)
            with open(entry.path) as f:
                urls_general = f.read().splitlines()
            urls_general.pop(0)
            urls_general=urls_general
            chunk_size = 1
            urls_general=urls_general[0:chunk_size]
            payload_list = []
            download_stream_size = 1
            inference_stream_size= 1
            grouped = [urls_general[i:i + chunk_size] for i in range(0, len(urls_general), chunk_size)]

            for chunk in grouped:
                payload_list.append({'payload': {'body':
                    {
                        'images': chunk,
                        'stream_size': 8,
                        'download_stream_size': download_stream_size,
                        'inference_stream_size':inference_stream_size,
                    }}})

            fexec = FunctionExecutor(reset=False,runtime_memory=3008)
            result, invocation_times = fexec.map_cnn_threading_benchmark(payload_list)
            body = result[0]['body']
            print(body['parallel_info'])
            fexec.close()






import os
import platform
from lithops import FunctionExecutor

def Average(lst):
    return sum(lst) / len(lst)


if __name__ == '__main__':
    directory_path='csvs'
    pyversion_tuple=platform.python_version_tuple()
    hola = pyversion_tuple[0]+pyversion_tuple[1]
    shard_size = 1
    num_functions = 1
    inters = [0]
    intras = [0]
    for entry in os.scandir(directory_path):
        if entry.is_file():
            filename_without_extension = entry.name[:-4]
            print("Analysing:", filename_without_extension)
            with open(entry.path) as f:
                urls_general = f.read().splitlines()
            urls_general.pop(0)
            urls_general = urls_general[0:shard_size]
            urls_general=urls_general*num_functions
            grouped = [urls_general[i:i + shard_size] for i in range(0, len(urls_general), shard_size)]
            fexec = FunctionExecutor(reset=False, runtime_memory=3008)
            for inter in inters:
                for intra in intras:
                    payload_list = []
                    for chunk in grouped:
                        payload_list.append({'payload': {'body':
                            {
                                'images': chunk,
                                'inter': inter,
                                'intra':intra,
                            }}})
                    results, invocation_times = fexec.map_cnn_threading_benchmark(payload_list, force_cold=False)
                    time_inferences = []
                    for res in results:
                        body = res['body']
                        time_inference = body['time_inference']
                        time_inferences.append(body['time_inference'])
                        # print(body['show_info'])
                        print(body['parallel_info'])
                        inter_lambda=body['inter']
                        intra_lambda=body['intra']
                    average_time_inference = Average(time_inferences)
                    print(results)
                    print(f"Inference Serial mode, Shard Size {shard_size}, Inter {inter_lambda}, Intra {intra_lambda}, Tests {num_functions}, time: {average_time_inference}, times: {time_inferences}\n", )
                    # with open("benchmarks/10240/torchscript_paralelism.txt", "a") as file:
                    #     file.write(f"Inference Serial mode, Shard Size {shard_size}, Inter {inter_lambda}, Intra {intra_lambda}, Tests {num_functions}, time: {average_time_inference}, times: {time_inferences}\n", )

            fexec.close()






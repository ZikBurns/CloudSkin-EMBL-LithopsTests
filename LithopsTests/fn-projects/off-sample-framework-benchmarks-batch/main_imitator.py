import os
import platform
from lithops import FunctionExecutor

def Average(lst):
    return sum(lst) / len(lst)


if __name__ == '__main__':
    directory_path='csvs'
    pyversion_tuple=platform.python_version_tuple()
    hola = pyversion_tuple[0]+pyversion_tuple[1]
    shard_size = 2
    num_functions = 2
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
                    fexec.map_cnn_threading_benchmark_imitator(payload_list, force_cold=False)
                    print(fexec.get_result())
                    fexec.plot(dst="./")




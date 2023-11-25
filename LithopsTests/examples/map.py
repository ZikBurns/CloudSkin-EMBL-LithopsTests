"""
Simple Lithops example using the map method.
In this example the map() method will launch one
map function for each entry in 'iterdata'. Finally
it will print the results for each invocation with
fexec.get_result()
"""
import os
import time

import lithops
import psutil


def my_map_function(id, x):
    time.sleep(5)
    print(f"I'm activation number {id}")
    return x + 7


if __name__ == "__main__":
    iterdata = list(range(2))
    fexec = lithops.FunctionExecutor()
    fexec.map(my_map_function, iterdata)
    print(fexec.get_result())
    fexec.plot(dst="./")
    fexec.clean()

process = psutil.Process(os.getpid())
thread_count = process.num_threads()
print(thread_count)
"""
Simple Lithops example using the map() call to estimate PI
"""
import lithops
import random


def is_inside(n):
    count = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x * x + y * y < 1:
            count += 1
    return count


np, n = 100, 15000000
part_count = [int(n / np)] * np
fexec = lithops.FunctionExecutor()
fexec.map(is_inside, part_count)
results = fexec.get_result()
pi = sum(results) / n * 4
print("Esitmated Pi: {}".format(pi))

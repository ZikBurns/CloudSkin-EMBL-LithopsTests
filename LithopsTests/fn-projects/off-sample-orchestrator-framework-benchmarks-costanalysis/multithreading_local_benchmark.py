import time
from concurrent.futures import ThreadPoolExecutor

def call_sleep(number):
    time.sleep(5)
    return number

n = 900
numbers = [i for i in range(1, n+1)]

start = time.time()
with ThreadPoolExecutor(max_workers=len(numbers)) as executor:
    lengths = list(executor.map(call_sleep, numbers))
end = time.time()

print(end-start-5)

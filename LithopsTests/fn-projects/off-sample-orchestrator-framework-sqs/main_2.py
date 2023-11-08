import json
import random
import time
from lithops.serve.serve import LithopsServe


def random_chunks(lst, min_chunk_size, max_chunk_size):
    chunks = []
    remaining = lst.copy()

    while remaining:
        chunk_size = random.randint(min_chunk_size, max_chunk_size)
        if chunk_size > len(remaining):
            chunk_size = len(remaining)

        chunk = remaining[:chunk_size]
        chunks.append(chunk)
        remaining = remaining[chunk_size:]

    return chunks

if __name__ == '__main__':
    with open('datasets/2016-09-21_16h06m49s__19.csv') as f:
        urls = f.read().splitlines()
    urls.pop(0)
    urls = urls[0:20]

    payloads = []
    rand_chunks = random_chunks(urls, 10, 10)
    for chunk in rand_chunks:
        payload_body = {
            "chunk_size": 1,
            "images": chunk
        }
        payloads.append(payload_body)
    start = time.time()
    server = LithopsServe(clean=False)
    result = server.enqueue_multiple(payloads)
    end = time.time()
    print(end-start)
    print(result)
    with open('results.txt', 'w') as file:
      file.write(json.dumps(result, indent=4))



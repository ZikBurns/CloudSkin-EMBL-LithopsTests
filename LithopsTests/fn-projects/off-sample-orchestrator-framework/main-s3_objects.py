import json
from lithops.serve.serve import LithopsServe

if __name__ == '__main__':
    with open('csvs/percentile_90.csv') as f:
        urls = f.read().splitlines()
    urls.pop(0)
    urls = urls[0:4]
    payload_body = {
        "chunk_size": 1,
        "images": urls
    }
    server = LithopsServe(clean=True)
    result = server.run_orchestrator(payload_body)
    print(result)
    with open('results.txt', 'w') as file:
      file.write(json.dumps(result, indent=4))



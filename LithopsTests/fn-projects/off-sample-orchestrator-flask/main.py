import json

from lithops.config import load_config
from lithops.serve.serve import LithopsServe

if __name__ == '__main__':
    with open('datasets/2016-09-21_16h06m49s__6.csv') as f:
        urls = f.read().splitlines()
    urls.pop(0)
    urls = urls[0:10]
    config = load_config()
    payload_body = {
        "chunk_size": 1,
        "images": urls,
        "config":config
    }
    server = LithopsServe(clean=False, config = config)


    result = server.run_orchestrator_flask('http://localhost:8000',payload_body)
    print(result)




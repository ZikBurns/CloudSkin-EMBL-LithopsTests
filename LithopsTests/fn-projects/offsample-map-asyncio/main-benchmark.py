import asyncio
import json
import resource
import os
import aiobotocore
import lithops
from time import time
from resources import PredictResource

def my_function(payload):
    payload = payload["body"]
    if isinstance(payload, str):
        payload = json.loads(payload)
    predictions = PredictResource("torchscript_model.pt").execute_inference(payload)
    result = {'predictions': predictions['predictions']}
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }


if __name__ == '__main__':

    with open('csvs/percentile_10.csv') as f:
        urls = f.read().splitlines()

    with open('datasets/2016-09-21_16h06m49s__6.csv') as f:
        urls = f.read().splitlines()
    urls.pop(0)
    urls = urls[0:1]

    payload_list = []
    for image in urls:
        payload_list.append({'payload': {'body': {'images': [image]}}})
    # group_size = 10000
    # groups = [payload_list[i:i + group_size] for i in range(0, len(payload_list), group_size)]
    fexec = lithops.FunctionExecutor(reset=False)
    # results=[]
    # fexec.select_runtime()
    # for group in groups:
    #     result = fexec.map_cnn_threading(group)
    #     results.append(result)
    start = time()
    result = fexec.map_cnn_threading(payload_list)
    end = time()
    print(end - start)
    print(result)
    fexec.close()
    end = time()





import json
import os

import boto3
import lithops
from resources import PredictResource

def my_function(payload):
    payload = payload["body"]
    if isinstance(payload, str):
        payload = json.loads(payload)
    predictions = PredictResource("/function/bin/torchscript_model.pt").execute_inference(payload)
    result = {'predictions': predictions['predictions']}
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }

if __name__ == '__main__':
    f = open('data1.json')
    payload = json.load(f)
    payload = { 'payload': { 'body': payload } }
    fexec = lithops.FunctionExecutor(runtime='off-sample-test-0',runtime_memory=3008)
    fexec.call_async(my_function, payload)
    print(fexec.get_result())

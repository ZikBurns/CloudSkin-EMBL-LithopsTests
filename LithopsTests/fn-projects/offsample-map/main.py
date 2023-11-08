import json
import lithops
from resources import PredictResource
import time

def my_function(payload):
    payload = payload["body"]
    if isinstance(payload, str):
        payload = json.loads(payload)
    predictions = PredictResource("/opt/torchscript_model.pt").execute_inference(payload)
    result = {'predictions': predictions['predictions']}
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }

if __name__ == '__main__':
    start = time.time()
    with open('datasets/2016-09-21_16h06m49s__6.csv') as f:
        urls = f.read().splitlines()
    urls.pop(0)
    urls=urls[0:10]
    payload_list=[]
    for image in urls:
        payload_list.append({ 'payload': { 'body': {'images': [ image ]} } })

    fexec = lithops.FunctionExecutor(runtime_memory=3008)
    fexec.map_cnn(payload_list)
    print(fexec.get_result())
    end = time.time()
    print(end - start)


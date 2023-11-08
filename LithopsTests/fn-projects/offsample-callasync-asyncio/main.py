import asyncio
import json
import lithops
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

async def main():
    with open('datasets/2016-09-21_16h06m49s__6.csv') as f:
        urls = f.read().splitlines()
    urls.pop(0)
    urls = urls[0:100]

    f = open('data.json')
    payload = json.load(f)
    payload = {'payload': {'body': payload}}
    fexec = lithops.FunctionExecutor()
    result = await fexec.call_async_cnn_asyncio_alt({'payload': {'body': {'images': urls[0:2]}}})
    print(result)


asyncio.run(main())
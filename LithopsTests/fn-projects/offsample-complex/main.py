import json
import lithops
from resources import PredictResource
from lithops.serverless.backends.aws_lambda_custom.custom_code.function import lambda_function

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
    f = open('data.json')
    payload = json.load(f)
    payload = { 'payload': { 'body': payload } }
    fexec = lithops.FunctionExecutor(runtime_memory=3008)
    fexec.call_async_cnn(payload)
    print(fexec.get_result())

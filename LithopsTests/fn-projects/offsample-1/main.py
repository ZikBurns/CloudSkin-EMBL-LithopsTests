import json
import lithops
import boto3

def my_function(payload):
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(FunctionName='arn:aws:lambda:us-east-1:879646340568:function:PredictResourceTorchscript',
                         InvocationType='RequestResponse',
                         Payload=json.dumps(payload))
    results=response['Payload'].read()
    results=json.loads(results.decode('utf-8'))
    return results

if __name__ == '__main__':
    f = open('data.json')
    payload = json.load(f)
    payload = { 'payload': { 'body': payload } }
    fexec = lithops.FunctionExecutor(runtime_memory=2048)
    fexec.call_async(my_function, payload)
    print(fexec.get_result())

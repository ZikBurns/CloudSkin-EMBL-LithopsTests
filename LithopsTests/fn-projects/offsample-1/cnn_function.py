
import boto3
import json

def my_function(payload):
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(FunctionName='arn:aws:lambda:us-east-1:879646340568:function:PredictResourceTorchscript',
                         InvocationType='RequestResponse',
                         Payload=json.dumps(payload))
    results=response['Payload'].read()
    results=json.loads(results.decode('utf-8'))
    return results

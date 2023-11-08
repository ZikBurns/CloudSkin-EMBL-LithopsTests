import json
import os
import lithops

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def my_function(payload):
    lista = os.listdir("/function/bin")
    return {
        'statusCode': 200,
        'body': json.dumps(lista)
    }

if __name__ == '__main__':
    f = open('data.json')
    payload = json.load(f)
    payload = { 'payload': { 'body': payload } }
    fexec = lithops.FunctionExecutor(runtime='wasinn-test-3',runtime_memory=3008)
    fexec.call_async(my_function, payload)
    print(fexec.get_result())

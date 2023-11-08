import json
import lithops

if __name__ == '__main__':
    with open('datasets/2016-09-21_16h06m49s__6.csv') as f:
        urls = f.read().splitlines()
    urls.pop(0)
    urls = urls[0:10]

    f = open('data.json')
    payload = json.load(f)
    payload = { 'payload': { 'body': payload } }
    fexec = lithops.FunctionExecutor()
    fexec.call_async_cnn({'payload': {'body': {'images': urls[0:2]}}})
    print(fexec.get_result())

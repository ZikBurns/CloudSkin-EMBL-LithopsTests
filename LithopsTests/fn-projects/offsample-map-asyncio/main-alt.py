import asyncio
import json
import lithops
from resources import PredictResource


async def main():
    with open('datasets/2016-09-21_16h06m49s__6.csv') as f:
        urls = f.read().splitlines()
    urls.pop(0)
    urls = urls[0:1000]
    payload_list = []
    for image in urls:
        payload_list.append({'payload': {'body': {'images': [image]}}})
    fexec = lithops.FunctionExecutor()
    result = await fexec.map_cnn_asyncio_futures(payload_list)
    print(result)

asyncio.run(main())

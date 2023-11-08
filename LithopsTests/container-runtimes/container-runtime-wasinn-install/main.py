import io
import json
import os
import shutil
import struct
import subprocess
import sys
import zipfile
import boto3
import lithops
import requests
from PIL import Image
from torch import Tensor
from torchvision import transforms
from transformations import apply_tfms, normalize
import os, shutil

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def list_files(startpath):
    returnlist=[]
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            returnlist.append('{}{}'.format(subindent, f))
    return returnlist

def my_function(payload):

    #rlist = list_files("/function/handler")
    lista = os.listdir("/function/bin")
    os.environ['LD_LIBRARY_PATH'] = f"/function/bin/libtorch/lib"
    os.environ['Torch_DIR'] = f"/function/bin/libtorch"
    shutil.copytree("/function/bin/wasinn", "/tmp/wasinn")
    shutil.rmtree("/tmp/wasinn/build")
    os.mkdir("/tmp/wasinn/build")
    os.chdir('/tmp/wasinn/build')
    result = subprocess.run(
    ['cmake', '-DCMAKE_BUILD_TYPE=Release', '-DWASMEDGE_PLUGIN_WASI_NN_BACKEND=PyTorch', '..'],
    capture_output=True, text=True)
    print(result)
    command = ['cmake', '--install', '/function/bin/wasinn/build']
    result = subprocess.run(command,capture_output=True)
    print(result.stdout)
    url="https://s3.eu-west-1.amazonaws.com/sm-image-storage-prod/iso/2016-09-21_16h06m49s/28aa128e8a38d7d6af1ee8ba367f5c2f"
    response = requests.get(url).content
    image = Image.open(io.BytesIO(response)).convert('RGB')
    imgtensor = transforms.ToTensor()(image)
    x = apply_tfms(imgtensor, size=224, padding_mode='reflection', mode='bilinear')
    datanormed = normalize(x, mean=Tensor([0.485, 0.456, 0.406]), std=Tensor([0.229, 0.224, 0.225]))
    tensorray = datanormed.numpy()
    reshaped_array = tensorray.reshape(3, -1)
    transposed_array = reshaped_array.transpose()
    flattened = transposed_array.flatten()
    data = struct.pack('<{}f'.format(len(flattened)), *flattened)

    command = '/function/bin/.wasmedge/bin/wasmedge --dir .:. /function/bin/wasmedge-wasinn-example-mobilenet-image.wasm /function/bin/torchscript_model.pt'
    proc = subprocess.Popen(command, shell=True, cwd='/tmp', stdin=subprocess.PIPE)
    output, _ = proc.communicate(data)
    print(output)
    return_code = proc.wait()
    print(return_code)
    return {
        'statusCode': 200,
        'body': json.dumps(lista)
    }

if __name__ == '__main__':
    fexec = lithops.FunctionExecutor(runtime='off-sample-test-7',runtime_memory=3008)
    fexec.call_async(my_function, "")
    print(fexec.get_result())

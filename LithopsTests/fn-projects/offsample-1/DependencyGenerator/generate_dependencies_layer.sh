#!/bin/bash
# Activate python 3.7 before executing
eval "$(conda shell.bash hook)"
conda activate python37

#Delete previous installation
rm -rf python site-packages*

# Install requirements.txt
pip install -r requirements.txt -t ./python/

# Show big files
#du -hs python/* | sort -h

# NEEDED PACKAGES:
cd python
find . -type d -name "tests" -exec rm -rf {} +
find . -type d -name "__pycache__" -exec rm -rf {} +
rm -rf {lithops*,click*,cycler*,jmespath*,kiwisolver*,rsa*,seaborn*,PyJWT*,requests_oauthlib*,oauthlib*,packaging*,bcrypt*,docker*,pyasn*,websocket_client*,lxml*,PyNaCl*,google*,paramiko*,cryptography*,setuptools*,Pillow*,jwt*,font[tT]ools*,pandas*,test*,_cffi_backend.cpython-37m-x86_64-linux-gnu.so,mpl_toolkits,pkg_resources,*yaml*,PIL*,nacl*,distutils-precedence.pth,matplotlib*,pylab*,share,pycparser*,pyparsing*,cachetools*,cffi*,_distutils_hack,tqdm*,pytz*,kubernetes*,ibm*,websocket,*dateutil*}

# Zip dependencies
cd ..
zip -r9 site-packages.zip python

## Upload to S3
aws s3 cp site-packages.zip s3://off-sample-s3/site-packages-lithops.zip
#
## Create new version of layer
aws lambda publish-layer-version \
    --no-paginate  \
    --no-cli-pager \
    --layer-name LayerLithops \
    --description "Lithops dependencies layer" \
    --content S3Bucket=off-sample-s3,S3Key=site-packages-lithops.zip \
    --compatible-runtimes python3.7 \
    --license-info "MIT" \
    --region eu-north-1
    
#rm -rf python site-packages* python.zip

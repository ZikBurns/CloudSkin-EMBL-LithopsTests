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
rm -rf ./{caffe2,wheel,wheel-*,boto*,aws*,pip,pip-*,pipenv}
rm -rf ./{*.egg-info,*.dist-info}
find . -name \*.pyc -delete
rm -rf {catalogue*,bs4*,srsly*,pydantic*,murmurhash*,click*,wasabi*,typer*,smart*,preshed*,[mM]arkup[sS]afe*,confection*,,tzdata*,spacy*,soupsieve*,setuptools*,python-dateutil*,pathy*,langcodes*,jinja2*,font[tT]ools*,contourpy*,spacy*,nvidia*,numexpr*,[bB]ottleneck*,beautifulsoup4*,torchaudio*,dateutil*,jinja*,plac*,pydantic*}
rm -rf {lithops*,click*,cycler*,jmespath*,kiwisolver*,rsa*,seaborn*,PyJWT*,requests_oauthlib*,oauthlib*,packaging*,bcrypt*,docker*,pyasn*,websocket_client*,lxml*,PyNaCl*,google*,paramiko*,cryptography*,setuptools*,jwt*,fonttools*,pandas*,test*,_cffi_backend.cpython-37m-x86_64-linux-gnu.so,mpl_toolkits,pkg_resources,*yaml*,*Yaml*,nacl*,distutils-precedence.pth,matplotlib*,pylab*,share,pycparser*,pyparsing*,cachetools*,cffi*,_distutils_hack,pytz*,kubernetes*,ibm*,websocket,*dateutil*}

# Zip up torch
zip -r9 torch.zip torch
rm -r torch

# Zip dependencies
cd ..
zip -r9 site-packages.zip python torchscript_model.pt

#### Upload to S3
#aws s3 cp site-packages.zip s3://off-sample/site-packages-lithops-complex.zip
##
### Create new version of layer
#aws lambda publish-layer-version \
#    --no-paginate  \
#    --no-cli-pager \
#    --layer-name LayerLithopsTorch \
#    --description "Lithops dependencies layer" \
#    --content S3Bucket=off-sample-s3,S3Key=site-packages-lithops.zip \
#    --compatible-runtimes python3.7 \
#    --license-info "MIT" \
#    --region eu-north-1

#rm -rf python site-packages* python.zip

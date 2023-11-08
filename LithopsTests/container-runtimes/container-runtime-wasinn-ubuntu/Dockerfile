# Python 3.7
FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install -y software-properties-common

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update

# Install Python 3.7 and pip
RUN apt-get install -y python3.7 python3.7-dev python3-pip

# Create a symbolic link for 'python' to point to Python 3.7
RUN ln -s /usr/bin/python3.7 /usr/bin/python

# Verify the Python installation
RUN python --version

RUN apt-get update -y \
    # Install aws-lambda-cpp build dependencies
    && apt-get install -y \
      build-essential \
      unzip \
#      llvm \
#      llvm-dev \
#      lld  \
      g++  \
      wget \
    # cleanup package lists, they are not used anymore in this image
    && rm -rf /var/lib/apt/lists/* \
    && apt-cache search linux-headers-generic

# Install necessary dependencies for building CMake and OpenSSL
RUN apt-get install -y build-essential wget

# Download and install OpenSSL 1.1.1
RUN wget https://www.openssl.org/source/openssl-1.1.1l.tar.gz && \
    tar xf openssl-1.1.1l.tar.gz && \
    cd openssl-1.1.1l && \
    ./config && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf openssl-1.1.1l openssl-1.1.1l.tar.gz

# Download and install CMake
RUN wget https://cmake.org/files/v3.21/cmake-3.21.1.tar.gz && \
    tar xf cmake-3.21.1.tar.gz && \
    cd cmake-3.21.1 && \
    ./bootstrap -- -DOPENSSL_ROOT_DIR=/usr/local/ssl -DOPENSSL_LIBRARIES=/usr/local/ssl/lib -DOPENSSL_INCLUDE_DIR=/usr/local/ssl/include && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf cmake-3.21.1 cmake-3.21.1.tar.gz

# Verify the CMake installation
RUN cmake --version
#RUN apt-get update \
#    && apt-get install -y \
#        g++ \
#        wget \
#    && rm -rf /var/lib/apt/lists/* \
#    && wget https://cmake.org/files/v3.26/cmake-3.26.4-linux-x86_64.tar.gz \
#    && tar -xvf cmake-3.26.4-linux-x86_64.tar.gz \
#    && cd cmake-3.26.4-linux-x86_64 \
#    && cp -r bin /usr/local/ \
#    && cp -r share /usr/local/ \
#    && cp -r doc /usr/local/share/ \
#    && cp -r man /usr/local/share/

RUN apt-get update && \
    apt-get install -y cmake make clang git curl libssl-dev build-essential python-dev libxml2-dev libxslt-dev && \
    apt-get clean

#RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
#RUN apt-add-repository "deb http://apt.llvm.org/bionic/ llvm-toolchain-bionic-11 main"
#RUN apt-get update
#RUN apt-get install -y llvm-11 llvm-11-dev clang-11 llvm-11-tools

ARG FUNCTION_DIR="/function"
ARG BINS_DIR="/function/bin"
# Copy function code
RUN mkdir -p ${FUNCTION_DIR}

# Update pip
RUN pip3 install --upgrade --ignore-installed pip wheel six setuptools \
    && pip3 install --upgrade --no-cache-dir --ignore-installed \
        awslambdaric \
        boto3 \
        redis \
        httplib2 \
        requests \
        numpy \
        scipy \
        pandas \
        pika \
        kafka-python \
        cloudpickle \
        ps-mem \
        tblib

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Add Lithops
COPY lithops_lambda.zip ${FUNCTION_DIR}
RUN unzip lithops_lambda.zip \
    && rm lithops_lambda.zip \
    && mkdir handler \
    && touch handler/__init__.py \
    && mv entry_point.py handler/

# Put your dependencies here, using RUN pip install... or RUN apt install...
RUN pip3 install six \
    urllib3==1.26.15 \
    torch==1.3.1 \
    torchvision==0.4.2


RUN mkdir -p ${BINS_DIR}
COPY stuff/torchscript_model.pt ${BINS_DIR}/torchscript_model.pt
COPY stuff/wasmedge-wasinn.wasm ${BINS_DIR}/wasmedge-wasinn.wasm
COPY stuff/libtorch ${BINS_DIR}/libtorch
COPY stuff/wasinn ${BINS_DIR}/wasinn
COPY stuff/.wasmedge ${BINS_DIR}/.wasmedge
ENV LD_LIBRARY_PATH=${BINS_DIR}/libtorch/lib
ENV Torch_DIR=${BINS_DIR}/libtorch
WORKDIR ${BINS_DIR}/wasinn/build
RUN cmake -DCMAKE_BUILD_TYPE=Release -DWASMEDGE_PLUGIN_WASI_NN_BACKEND="PyTorch" ..

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "handler.entry_point.lambda_handler" ]









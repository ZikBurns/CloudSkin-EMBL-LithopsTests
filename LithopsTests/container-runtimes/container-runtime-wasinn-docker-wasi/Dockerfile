# Python 3.7
FROM python:3.8-slim-buster


RUN apt-get update -y
RUN apt-get install -y software-properties-common

RUN apt-get update \
    # Install aws-lambda-cpp build dependencies
    && apt-get install -y \
      g++ \
      make \
      cmake \
      unzip \
      ninja-build \
#      clang \
      git \
      curl \
      libssl-dev \
      python-dev \
      libxml2-dev \
      libxslt-dev \
      fakeroot \
      wget \
      build-essential \
      gnupg \
      apt-transport-https \
    # cleanup package lists, they are not used anymore in this image
    && rm -rf /var/lib/apt/lists/* \
    && apt-cache search linux-headers-generic


RUN wget https://apt.llvm.org/llvm.sh \
    && chmod +x llvm.sh \
    && ./llvm.sh all \

ENV LLVM_VERSION=$(llvm-config --version)
ENV CMAKE_PREFIX_PATH=/usr/lib/llvm-$LLVM_VERSION/lib/cmake
#ENV LLD_DIR=/usr/lib/llvm-16/lib/cmake
# Download and install CMake
RUN curl -sSLO https://github.com/Kitware/CMake/releases/download/v3.25.1/cmake-3.25.1-linux-x86_64.tar.gz \
  && tar xf cmake-3.25.1-linux-x86_64.tar.gz \
  && rm cmake-3.25.1-linux-x86_64.tar.gz \
  && mkdir -p /opt \
  && mv cmake-3.25.1-linux-x86_64 /opt/cmake
ENV PATH /opt/cmake/bin:$PATH

ARG FUNCTION_DIR="/function"
ARG BINS_DIR="/function/bin"

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}

# Update pip
RUN pip install --upgrade --ignore-installed pip wheel six setuptools \
    && pip install --upgrade --no-cache-dir --ignore-installed \
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
        tblib \
        six \
        urllib3==1.26.15 \
        torch==1.4.0 \
        torchvision==0.5.0

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

## Add Lithops
#COPY lithops_lambda.zip ${FUNCTION_DIR}
#RUN unzip lithops_lambda.zip \
#    && rm lithops_lambda.zip \
#    && mkdir handler \
#    && touch handler/__init__.py \
#    && mv entry_point.py handler/

RUN cd /tmp && git clone --recursive https://github.com/WebAssembly/wasi-sdk.git
WORKDIR /tmp/wasi-sdk
RUN NINJA_FLAGS=-v make package
ENV WASI_VERSION=14
ENV WASI_VERSION_FULL=${WASI_VERSION}.0
RUN wget https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-${WASI_VERSION}/wasi-sdk-${WASI_VERSION_FULL}-linux.tar.gz \
    && tar xvf wasi-sdk-${WASI_VERSION_FULL}-linux.tar.gz
ENV WASI_SDK_PATH=/tmp/wasi-sdk-${WASI_VERSION_FULL}
WORKDIR ${FUNCTION_DIR}
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN echo 'source $HOME/.cargo/env' >> $HOME/.bashrc
COPY WE_install.sh /tmp/WE_install.sh
RUN /tmp/WE_install.sh

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "handler.entry_point.lambda_handler" ]









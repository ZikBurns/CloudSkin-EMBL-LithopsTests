# Python 3.7
FROM python:3.7-slim

RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN apt-get update -y \
    # Install aws-lambda-cpp build dependencies
    && apt-get install -y \
      build-essential \
      unzip \
      llvm \
      llvm-dev \
      lld  \
    # cleanup package lists, they are not used anymore in this image
    && rm -rf /var/lib/apt/lists/* \
    && apt-cache search linux-headers-generic



RUN apt-get update \
    && apt-get install -y \
        g++ \
        wget \
    && rm -rf /var/lib/apt/lists/* \
    && wget https://cmake.org/files/v3.26/cmake-3.26.4-linux-x86_64.tar.gz \
    && tar -xvf cmake-3.26.4-linux-x86_64.tar.gz \
    && cd cmake-3.26.4-linux-x86_64 \
    && cp -r bin /usr/local/ \
    && cp -r share /usr/local/ \
    && cp -r doc /usr/local/share/ \
    && cp -r man /usr/local/share/

RUN apt-get update && \
    apt-get install -y cmake make clang git curl libssl-dev build-essential libxml2-dev libxslt-dev python3 ninja-build && \
    apt-get clean

RUN apt-get update && \
    apt-get install -y git
RUN git --version

#RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
#RUN apt-add-repository "deb http://apt.llvm.org/bionic/ llvm-toolchain-bionic-11 main"
#RUN apt-get update
#RUN apt-get install -y llvm-11 llvm-11-dev clang-11 llvm-11-tools

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
RUN pip install six \
    urllib3==1.26.15 \
    https://download.pytorch.org/whl/cpu/torch-1.0.1-cp37-cp37m-linux_x86_64.whl \
    torchvision==0.2.2 \
    Pillow==5.4.1

#WORKDIR /root
#RUN git clone https://github.com/llvm/llvm-project.git
#WORKDIR /root/llvm-project
#RUN git checkout llvmorg-14.0.0
#WORKDIR /root/llvm-project/build
#RUN cmake -G "Ninja" ../llvm \
#    -DCMAKE_BUILD_TYPE=Release \
#    -DLLVM_ENABLE_PROJECTS=clang \
#    -DLLVM_TARGETS_TO_BUILD=X86
#RUN cmake --build . --target install
#ENV LLVM_DIR=/usr/local/lib/cmake/llvm
#RUN apt-get autoremove -y \
#    && apt-get clean -y \
#    && rm -rf /var/lib/apt/lists/* /root/llvm-project

# https://www.rust-lang.org/tools/install
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- --plugins wasi_nn-pytorch
RUN rustup target add wasm32-wasi


COPY install_WasmEdge.sh ${FUNCTION_DIR}/install_WasmEdge.sh
RUN chmod +x ${FUNCTION_DIR}/install_WasmEdge.sh
RUN ${FUNCTION_DIR}/install_WasmEdge.sh

# https://wasmtime.dev/
RUN curl https://wasmtime.dev/install.sh -sSf | bash
#RUN LLD_DIR=$(find / -name lld-config.cmake -exec dirname {} \; | head -n 1) && \
#    echo "LLD_DIR=$LLD_DIR" >> /etc/environment
#ENV LLD_DIR=$LLD_DIR
WORKDIR ${FUNCTION_DIR}
RUN /bin/sh -c '. "$HOME/.cargo/env"'

RUN mkdir -p ${BINS_DIR}
COPY torchscript_model.pt ${BINS_DIR}/torchscript_model.pt
COPY libtorch ${BINS_DIR}/libtorch
COPY wasinn ${BINS_DIR}/wasinn
COPY .wasmedge ${BINS_DIR}/.wasmedge
WORKDIR ${BINS_DIR}/wasinn
#RUN mkdir -p ${BINS_DIR}/wasinn/build
WORKDIR ${BINS_DIR}/wasinn/build
ENV LD_LIBRARY_PATH=${BINS_DIR}/libtorch/lib
ENV Torch_DIR=${BINS_DIR}/libtorch

#RUN LLVM_VERSION=$(llvm-config --version)
#RUN echo "The value of MY_VARIABLE is: ${LLVM_VERSION}"
#RUN cmake -DCMAKE_BUILD_TYPE=Release -DLLD_DIR=/usr/lib/llvm-${LLVM_VERSION}/lib/cmake/lld -DWASMEDGE_PLUGIN_WASI_NN_BACKEND="PyTorch" ..
RUN cmake -DCMAKE_BUILD_TYPE=Release -DWASMEDGE_PLUGIN_WASI_NN_BACKEND="PyTorch" ..

RUN make -j
#RUN cmake --install .

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "handler.entry_point.lambda_handler" ]
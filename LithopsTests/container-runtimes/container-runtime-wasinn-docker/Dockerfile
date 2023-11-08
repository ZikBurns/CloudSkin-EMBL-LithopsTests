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
      libgtk2.0-dev \
      pkg-config \
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

#RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - \
#    && apt-get update \
#    && apt-get install -y clang lldb lld
RUN wget https://apt.llvm.org/llvm.sh \
    && chmod +x llvm.sh \
    && ./llvm.sh all \

RUN apt-get update \
    && apt-get install -y \
    clang-format clang-tidy clang-tools clang libc++-dev libc++1 libc++abi-dev libc++abi1 libclang-dev libclang1 liblldb-dev libllvm-ocaml-dev libomp-dev libomp5 lld lldb llvm-dev llvm-runtime llvm





#ENV LLVM_VERSION=$(llvm-config --version)
#ENV CMAKE_PREFIX_PATH=/usr/lib/llvm-$LLVM_VERSION/lib/cmake
#ENV LLD_DIR=/usr/lib/llvm-16/lib/cmake
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
RUN git clone https://github.com/llvm/llvm-project llvm-project
RUN mkdir build
WORKDIR ${FUNCTION_DIR}/build
RUN cmake -DCMAKE_BUILD_TYPE=Release -DLLVM_ENABLE_PROJECTS=lld -DCMAKE_INSTALL_PREFIX=/usr/local ../llvm-project/llvm
RUN make install

## Add Lithops
#COPY lithops_lambda.zip ${FUNCTION_DIR}
#RUN unzip lithops_lambda.zip \
#    && rm lithops_lambda.zip \
#    && mkdir handler \
#    && touch handler/__init__.py \
#    && mv entry_point.py handler/



RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN echo 'source $HOME/.cargo/env' >> $HOME/.bashrc
#COPY install_wasi.sh /tmp/install_wasi.sh
#RUN chmod +x /tmp/install_wasi.sh
#RUN /tmp/install_wasi.sh
COPY WE_install.sh /tmp/WE_install.sh
RUN /tmp/WE_install.sh

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "handler.entry_point.lambda_handler" ]









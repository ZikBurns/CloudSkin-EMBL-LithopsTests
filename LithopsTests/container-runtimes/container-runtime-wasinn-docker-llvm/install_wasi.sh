cd /tmp
git clone --recursive https://github.com/WebAssembly/wasi-sdk.git
cd wasi-sdk
NINJA_FLAGS=-v make package
export WASI_VERSION=14
export WASI_VERSION_FULL=${WASI_VERSION}.0
wget https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-${WASI_VERSION}/wasi-sdk-${WASI_VERSION_FULL}-linux.tar.gz
tar xvf wasi-sdk-${WASI_VERSION_FULL}-linux.tar.gz
export WASI_SDK_PATH=/tmp/wasi-sdk-${WASI_VERSION_FULL}

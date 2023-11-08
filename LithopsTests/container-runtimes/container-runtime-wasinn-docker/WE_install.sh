#cd /tmp
#git clone --recursive https://github.com/WebAssembly/wasi-sdk.git
#cd wasi-sdk
#NINJA_FLAGS=-v make package
#export WASI_VERSION=14
#export WASI_VERSION_FULL=${WASI_VERSION}.0
#wget https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-${WASI_VERSION}/wasi-sdk-${WASI_VERSION_FULL}-linux.tar.gz
#tar xvf wasi-sdk-${WASI_VERSION_FULL}-linux.tar.gz
#export WASI_SDK_PATH=/tmp/wasi-sdk-${WASI_VERSION_FULL}

cd /tmp
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- --plugins wasi_nn-pytorch
#curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- -p /tmp/.wasmedge
#curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
#export PATH="($HOME/.cargo/bin:${PATH}"
rustup target add wasm32-wasi

rm -rf /tmp/libtorch
export PYTORCH_VERSION="1.5.1"
curl -s -L -O --remote-name-all https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip
#curl -s -L -O --remote-name-all https://download.pytorch.org/libtorch/lts/1.8/cpu/libtorch-cxx11-abi-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip
unzip -q "libtorch-cxx11-abi-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip"
rm -f "libtorch-cxx11-abi-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip"
export LD_LIBRARY_PATH=/tmp/libtorch/lib
export Torch_DIR=/tmp/libtorch

rm -rf /tmp/wasinn
mkdir /tmp/wasinn
git clone https://github.com/WasmEdge/WasmEdge.git /tmp/wasinn
# Install the PyTorch dependency


#cd /
#result=$(find . -name "LLDConfig*")
#echo "I have results"
#for path in $result; do
#    echo "$path"
#done

cd /tmp/wasinn
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DWASMEDGE_PLUGIN_WASI_NN_BACKEND="PyTorch" ..
make -j
#cmake --install .
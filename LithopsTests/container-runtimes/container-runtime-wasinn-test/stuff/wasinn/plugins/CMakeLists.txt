# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2019-2022 Second State INC

if(WASMEDGE_PLUGIN_WASI_NN_BACKEND)
  add_subdirectory(wasi_nn)
endif()

if(WASMEDGE_PLUGIN_WASI_CRYPTO)
  add_subdirectory(wasi_crypto)
endif()

if(WASMEDGE_PLUGIN_PROCESS)
  # Only Linux systems support wasmedge_process now.
  if(CMAKE_SYSTEM_NAME MATCHES "Linux")
    add_subdirectory(wasmedge_process)
  else()
    message(WARNING "Only Linux platforms support WasmEdge_Process plug-in now.")
  endif()
endif()

if(WASMEDGE_PLUGIN_WASM_BPF)
  # Only Linux systems support wasm_bpf now.
  if(CMAKE_SYSTEM_NAME MATCHES "Linux")
    add_subdirectory(wasm_bpf)
  else()
    message(WARNING "Only Linux platforms support wasm_bpf plug-in now.")
  endif()
endif()

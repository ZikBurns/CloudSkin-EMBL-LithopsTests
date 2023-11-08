# LithopsTests
This module has different tests using lithops. Recommended use with [lithops-cnn](https://github.com/ZikBurns/lithops-cnn).

Here is a summary of each Module:
* `container-runtimes`: Uses [Lithops Container Runtime](https://github.com/lithops-cloud/lithops/tree/master/runtime/aws_lambda) and the [Lithops CLI for runtime management](https://lithops-cloud.github.io/docs/source/cli.html)
  * `container-runtime`: Container Runtime using Pytorch inference in AWS Lambda
  * `container-runtime-wasinn`: Work in Progress. Container Runtime with WasmEdge and Wasi-NN plugin.
  * `container-runtime-wasinn-test`: Work in Progress. Extra container Runtime with WasmEdge and Wasi-NN plugin for testing.
* `examples`: Examples taken from [Lithops repo](https://github.com/lithops-cloud/lithops/tree/master/examples).
* `fn-projects`: Projects using AWS Lambda and localhost for Pytorch inference
  * `offsample-1`: First try to call_async. It just calls a lambda.
  * `offsample-changedgeneric`: Module used for testing.
  * `offsample-complex`: The result doesn't work because of Pytorch being too heavy. As a result, a new layer has to be generated (Find it in the DependencyGenerator).
  * `offsample-map`: Same as `offsample-complex`, but with map instead of call_async.

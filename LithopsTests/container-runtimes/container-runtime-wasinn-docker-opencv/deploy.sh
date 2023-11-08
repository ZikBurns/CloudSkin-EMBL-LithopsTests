eval "$(conda shell.bash hook)"
conda activate python37
lithops runtime build -f Dockerfile -b aws_lambda_default off-sample-test-7
lithops runtime deploy -b aws_lambda_default off-sample-test-7 --memory 3008
lithops runtime delete -b aws_lambda_default off-sample-test-6 --memory 3008
lithops runtime list
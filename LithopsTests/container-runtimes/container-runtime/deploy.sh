eval "$(conda shell.bash hook)"
conda activate python37
lithops runtime build -f Dockerfile -b aws_lambda_default off-sample-test-0
lithops runtime deploy off-sample-test-0 --memory 3008
lithops runtime list
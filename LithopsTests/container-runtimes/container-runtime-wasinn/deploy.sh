eval "$(conda shell.bash hook)"
conda activate python37
lithops runtime build -f Dockerfile -b aws_lambda_default wasinn-test-8
lithops runtime deploy wasinn-test-4 --memory 3008
lithops runtime list
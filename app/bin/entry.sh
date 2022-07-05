#!/bin/sh
echo "Retrieving environment parameters"
aws ssm get-parameters --region ca-central-1 --with-decryption --names share-files-securely-config --query 'Parameters[*].Value' --output text > ".env"

echo "Starting server ..."
exec /usr/local/bin/python -m awslambdaric $1
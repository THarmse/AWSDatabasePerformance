# parameter_store.py
# Theodor Harmse - University of Liverpool
# Helper module for reading database credentials from AWS Systems Manager Parameter Store

import boto3
import os

REGION = os.environ.get("AWS_REGION", "eu-west-1") 

def get_db_credentials(param_name: str) -> str:
    """
    Retrieves a SecureString parameter from AWS Systems Manager Parameter Store.
    Used to securely fetch database connection details that were created for each CloudFormation Script.

    :param param_name: The full path of the parameter in Parameter Store.
    :return: The decrypted parameter value as a JSON string.
    """
    ssm = boto3.client('ssm', region_name=REGION)
    response = ssm.get_parameter(
        Name=param_name,
        WithDecryption=True
    )

    return response['Parameter']['Value']

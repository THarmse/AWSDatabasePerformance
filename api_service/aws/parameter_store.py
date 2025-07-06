# parameter_store.py
# Theodor Harmse - University of Liverpool
# Helper module for reading and caching database credentials from AWS Systems Manager Parameter Store

import boto3
import os
from functools import lru_cache

REGION = os.environ.get("AWS_REGION", "eu-west-1")

@lru_cache(maxsize=128)
def get_db_credentials(param_name: str) -> str:
    """
    Returns the cached value if present.
    Otherwise, fetches from Parameter Store and caches it in memory per process.
    """
    ssm_client = boto3.client('ssm', region_name=REGION)
    response = ssm_client.get_parameter(
        Name=param_name,
        WithDecryption=True
    )
    return response['Parameter']['Value']

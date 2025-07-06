# parameter_store.py
# Theodor Harmse - University of Liverpool
# Helper module for reading and caching database credentials from AWS Systems Manager Parameter Store

import boto3
import os
from threading import Lock

REGION = os.environ.get("AWS_REGION", "eu-west-1")

_ssm_client = None
_cache = {}
_lock = Lock()

def get_db_credentials(param_name: str) -> str:
    """
    Returns the cached value if present.
    Otherwise, fetches from Parameter Store and caches it.
    Thread-safe.
    """
    global _ssm_client

    # Check cache first
    if param_name in _cache:
        return _cache[param_name]

    # Thread-safe initialization
    with _lock:
        if param_name in _cache:
            return _cache[param_name]

        if _ssm_client is None:
            _ssm_client = boto3.client('ssm', region_name=REGION)

        response = _ssm_client.get_parameter(
            Name=param_name,
            WithDecryption=True
        )
        value = response['Parameter']['Value']
        _cache[param_name] = value
        return value

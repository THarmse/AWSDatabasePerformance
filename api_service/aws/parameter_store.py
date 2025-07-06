# parameter_store.py
# Theodor Harmse - University of Liverpool
# Helper module for reading and caching database credentials from AWS Systems Manager Parameter Store

import boto3
import os
from cachetools import TTLCache
from threading import Lock

REGION = os.environ.get("AWS_REGION", "eu-west-1")

_cache = TTLCache(maxsize=128, ttl=3600)  # 1 hour TTL
_lock = Lock()

def get_db_credentials(param_name: str) -> str:
    """
    Returns the cached value if present and not expired.
    Otherwise, fetches from Parameter Store, caches it in memory.
    Thread-safe.
    """
    with _lock:
        if param_name in _cache:
            return _cache[param_name]

        ssm_client = boto3.client('ssm', region_name=REGION)
        response = ssm_client.get_parameter(
            Name=param_name,
            WithDecryption=True
        )
        value = response['Parameter']['Value']
        _cache[param_name] = value
        return value

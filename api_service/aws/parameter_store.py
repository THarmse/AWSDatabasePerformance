
# parameter_store.py
# Theodor Harmse - University of Liverpool
# Helper module for providing static database credentials in JSON format for all database types

import json

# Local static store of "Parameter Store" secrets
_STATIC_CREDENTIALS = {
    # MySQL
    "/Liverpool/RDS/MySQL/Credentials": json.dumps({
        "host": "mysql.liverpool.com",
        "username": "adminuser",
        "password": "Password123!",
        "database": "performance_db",
        "port": 3306
    }),

    # Aurora MySQL
    "/Liverpool/RDS/AuroraMySQL/Credentials": json.dumps({
        "host": "auroramysql.liverpool.com",
        "username": "adminuser",
        "password": "Password123!",
        "database": "performance_db",
        "port": 3306
    }),

    # PostgreSQL
    "/Liverpool/RDS/PostgreSQL/Credentials": json.dumps({
        "host": "postgresql.liverpool.com",
        "username": "adminuser",
        "password": "Password123!",
        "database": "performance_db",
        "port": 5432
    }),

    # Aurora PostgreSQL
    "/Liverpool/RDS/AuroraPostgreSQL/Credentials": json.dumps({
        "host": "aurorapostgresql.liverpool.com",
        "username": "adminuser",
        "password": "Password123!",
        "database": "performance_db",
        "port": 5432
    }),

    # Microsoft SQL Server
    "/Liverpool/RDS/MSSQLServer/Credentials": json.dumps({
        "host": "mssql.liverpool.com",
        "username": "adminuser",
        "password": "Password123!",
        "database": "performance_db",
        "port": 1433
    }),

    # Oracle
    "/Liverpool/RDS/OracleDB/Credentials": json.dumps({
        "host": "oracle.liverpool.com",
        "username": "adminuser",
        "password": "Password123!",
        "database": "ORCL",
        "port": 1521
    }),

    # MariaDB
    "/Liverpool/RDS/MariaDB/Credentials": json.dumps({
        "host": "mariadb.liverpool.com",
        "username": "adminuser",
        "password": "Password123!",
        "database": "performance_db",
        "port": 3306
    }),

    # IBM DB2
    "/Liverpool/RDS/IBMDB2/Credentials": json.dumps({
        "host": "db2.liverpool.com",
        "username": "adminuser",
        "password": "Password123!",
        "database": "perf_db",
        "port": 50000
    }),

    # DynamoDB
    "/Liverpool/DynamoDB/Credentials": json.dumps({
        "alias": "dynamodb.liverpool.com",
        "endpoint": "https://dynamodb.eu-west-1.amazonaws.com",
        "table_name": "transaction_records",
        "region": "eu-west-1"
    })
}


def get_db_credentials(param_name: str) -> str:
    """
    Returns the credential JSON string for the given parameter name.
    Raises KeyError if not found.
    """
    if param_name in _STATIC_CREDENTIALS:
        return _STATIC_CREDENTIALS[param_name]
    raise KeyError(f"Parameter {param_name} not found in static configuration.")


## parameter_store.py
## Theodor Harmse - University of Liverpool
## Helper module for reading and caching database credentials from AWS Systems Manager Parameter Store

#import boto3
#import os
#from cachetools import TTLCache
#from threading import Lock

#REGION = os.environ.get("AWS_REGION", "eu-west-1")

#_cache = TTLCache(maxsize=128, ttl=3600)  # 1 hour TTL
#_lock = Lock()

#def get_db_credentials(param_name: str) -> str:
#    """
#    Returns the cached value if present and not expired.
#    Otherwise, fetches from Parameter Store, caches it in memory.
#    Thread-safe.
#    """
#    with _lock:
#        if param_name in _cache:
#            return _cache[param_name]
#
#        ssm_client = boto3.client('ssm', region_name=REGION)
#        response = ssm_client.get_parameter(
#            Name=param_name,
#            WithDecryption=True
#        )
#        value = response['Parameter']['Value']
#        _cache[param_name] = value
#        return value

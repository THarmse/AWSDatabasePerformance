# base.py
# Theodor Harmse - University of Liverpool
# Shared utility functions for database connectivity

import json
import os
import boto3
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from threading import Lock
from urllib.parse import quote_plus

import psycopg2
import psycopg2.extras

REGION = os.environ.get("AWS_REGION", "eu-west-1")

# Caching for parameter store
from api_service.aws.parameter_store import get_db_credentials

# Connection pool engines
_mysql_engine = None
_postgresql_engine = None
_mariadb_engine = None
_mssql_engine = None
_oracle_engine = None
_ibmdb2_engine = None

_lock = Lock()

def _get_mysql_engine(param_name: str) -> Engine:
    global _mysql_engine
    with _lock:
        if _mysql_engine is None:
            creds = json.loads(get_db_credentials(param_name))
            username = quote_plus(creds['username'])
            password = quote_plus(creds['password'])
            _mysql_engine = create_engine(
                f"mysql+pymysql://{username}:{password}@{creds['host']}:{creds['port']}/{creds['database']}",
                pool_size=200,
                max_overflow=100,
                pool_recycle=3600
            )
        return _mysql_engine

def get_mysql_connection(param_name: str):
    """
    MySQL connection using PyMySQL via SQLAlchemy Engine Pool.
    """
    return _get_mysql_engine(param_name).connect()

def get_aurora_mysql_connection(param_name: str):
    """
    Aurora MySQL connection (same as MySQL).
    """
    return get_mysql_connection(param_name)

def _get_postgresql_engine(param_name: str) -> Engine:
    global _postgresql_engine
    with _lock:
        if _postgresql_engine is None:
            creds = json.loads(get_db_credentials(param_name))
            username = quote_plus(creds['username'])
            password = quote_plus(creds['password'])
            _postgresql_engine = create_engine(
                f"postgresql+psycopg2://{username}:{password}@{creds['host']}:{creds['port']}/{creds['database']}",
                pool_size=200,
                max_overflow=100,
                pool_recycle=3600
            )
        return _postgresql_engine

def get_postgresql_connection(param_name: str):
    """
    PostgreSQL connection using psycopg2 via SQLAlchemy Engine Pool.
    """
    return _get_postgresql_engine(param_name).connect()

def get_aurora_postgresql_connection(param_name: str):
    """
    Aurora PostgreSQL connection (same as PostgreSQL).
    """
    return get_postgresql_connection(param_name)

def _get_mariadb_engine(param_name: str) -> Engine:
    global _mariadb_engine
    with _lock:
        if _mariadb_engine is None:
            creds = json.loads(get_db_credentials(param_name))
            username = quote_plus(creds['username'])
            password = quote_plus(creds['password'])
            _mariadb_engine = create_engine(
                f"mysql+pymysql://{username}:{password}@{creds['host']}:{creds['port']}/{creds['database']}",
                pool_size=200,
                max_overflow=100,
                pool_recycle=3600
            )
        return _mariadb_engine

def get_mariadb_connection(param_name: str):
    """
    MariaDB connection using PyMySQL via SQLAlchemy Engine Pool.
    """
    return _get_mariadb_engine(param_name).connect()

def _get_mssql_engine(param_name: str) -> Engine:
    global _mssql_engine
    with _lock:
        if _mssql_engine is None:
            creds = json.loads(get_db_credentials(param_name))
            username = quote_plus(creds['username'])
            password = quote_plus(creds['password'])
            driver = quote_plus("ODBC Driver 17 for SQL Server")
            _mssql_engine = create_engine(
                f"mssql+pyodbc://{username}:{password}@{creds['host']}:{creds.get('port', 1433)}/{creds['database']}?driver={driver}",
                pool_size=200,
                max_overflow=100,
                pool_recycle=3600
            )
        return _mssql_engine

def get_mssqlserver_connection(param_name: str):
    """
    Microsoft SQL Server connection using SQLAlchemy Engine Pool.
    """
    return _get_mssql_engine(param_name).connect()

def _get_oracle_engine(param_name: str) -> Engine:
    global _oracle_engine
    with _lock:
        if _oracle_engine is None:
            creds = json.loads(get_db_credentials(param_name))
            username = quote_plus(creds['username'])
            password = quote_plus(creds['password'])
            _oracle_engine = create_engine(
                f"oracle+cx_oracle://{username}:{password}@{creds['host']}:{creds.get('port', 1521)}/?service_name={creds['database']}",
                pool_size=200,
                max_overflow=100,
                pool_recycle=3600
            )
        return _oracle_engine

def get_oracle_connection(param_name: str):
    """
    Oracle 19c connection using cx_Oracle via SQLAlchemy Engine Pool.
    """
    return _get_oracle_engine(param_name).connect()

def _get_ibmdb2_engine(param_name: str) -> Engine:
    global _ibmdb2_engine
    with _lock:
        if _ibmdb2_engine is None:
            creds = json.loads(get_db_credentials(param_name))
            username = quote_plus(creds['username'])
            password = quote_plus(creds['password'])
            _ibmdb2_engine = create_engine(
                f"ibm_db_sa://{username}:{password}@{creds['host']}:{creds.get('port', 50000)}/{creds['database']}",
                pool_size=200,
                max_overflow=100,
                pool_recycle=3600
            )
        return _ibmdb2_engine

def get_ibm_db2_connection(param_name: str):
    """
    IBM DB2 connection using ibm_db_sa via SQLAlchemy Engine Pool.
    """
    return _get_ibmdb2_engine(param_name).connect()

def get_dynamodb_resource():
    """
    DynamoDB boto3 resource.
    """
    return boto3.resource('dynamodb', region_name=REGION)

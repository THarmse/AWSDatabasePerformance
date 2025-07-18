import json
import os
import boto3
import pyodbc
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from threading import Lock
from urllib.parse import quote_plus

import psycopg2
import psycopg2.extras

REGION = os.environ.get("AWS_REGION", "eu-west-1")
from api_service.aws.parameter_store import get_db_credentials

# Connection pool engines
_mysql_engine = None
_aurora_mysql_engine = None
_postgresql_engine = None
_aurora_postgresql_engine = None
_mariadb_engine = None
_mssql_engine_target = None
_oracle_engine = None
_ibmdb2_engine = None

_lock = Lock()
_mssql_lock = Lock()

# ----------------- MYSQL -----------------------
def _get_mysql_engine(param_name: str) -> Engine:
    global _mysql_engine
    with _lock:
        if _mysql_engine is None:
            creds = json.loads(get_db_credentials(param_name))
            _mysql_engine = create_engine(
                f"mysql+pymysql://{quote_plus(creds['username'])}:{quote_plus(creds['password'])}@{creds['host']}:{creds['port']}/{creds['database']}",
                pool_size=200, max_overflow=100, pool_recycle=3600
            )
        return _mysql_engine

def get_mysql_connection(param_name: str):
    return _get_mysql_engine(param_name).raw_connection()

def _get_aurora_mysql_engine(param_name: str) -> Engine:
    global _aurora_mysql_engine
    with _lock:
        if _aurora_mysql_engine is None:
            creds = json.loads(get_db_credentials(param_name))
            _aurora_mysql_engine = create_engine(
                f"mysql+pymysql://{quote_plus(creds['username'])}:{quote_plus(creds['password'])}@{creds['host']}:{creds['port']}/{creds['database']}",
                pool_size=200, max_overflow=100, pool_recycle=3600
            )
        return _aurora_mysql_engine

def get_aurora_mysql_connection(param_name: str):
    return _get_aurora_mysql_engine(param_name).raw_connection()

# ----------------- POSTGRESQL -----------------------
def _get_postgresql_engine(param_name: str) -> Engine:
    global _postgresql_engine
    with _lock:
        if _postgresql_engine is None:
            creds = json.loads(get_db_credentials(param_name))
            _postgresql_engine = create_engine(
                f"postgresql+psycopg2://{quote_plus(creds['username'])}:{quote_plus(creds['password'])}@{creds['host']}:{creds['port']}/{creds['database']}",
                pool_size=200, max_overflow=100, pool_recycle=3600
            )
        return _postgresql_engine

def get_postgresql_connection(param_name: str):
    return _get_postgresql_engine(param_name).raw_connection()

def _get_aurora_postgresql_engine(param_name: str) -> Engine:
    global _aurora_postgresql_engine
    with _lock:
        if _aurora_postgresql_engine is None:
            creds = json.loads(get_db_credentials(param_name))
            _aurora_postgresql_engine = create_engine(
                f"postgresql+psycopg2://{quote_plus(creds['username'])}:{quote_plus(creds['password'])}@{creds['host']}:{creds['port']}/{creds['database']}",
                pool_size=200, max_overflow=100, pool_recycle=3600
            )
        return _aurora_postgresql_engine

def get_aurora_postgresql_connection(param_name: str):
    return _get_aurora_postgresql_engine(param_name).raw_connection()

# ----------------- MARIADB -----------------------
def _get_mariadb_engine(param_name: str) -> Engine:
    global _mariadb_engine
    with _lock:
        if _mariadb_engine is None:
            creds = json.loads(get_db_credentials(param_name))
            _mariadb_engine = create_engine(
                f"mysql+pymysql://{quote_plus(creds['username'])}:{quote_plus(creds['password'])}@{creds['host']}:{creds['port']}/{creds['database']}",
                pool_size=200, max_overflow=100, pool_recycle=3600
            )
        return _mariadb_engine

def get_mariadb_connection(param_name: str):
    return _get_mariadb_engine(param_name).raw_connection()

# ----------------- MSSQL -----------------------
def get_mssqlserver_master_connection(param_name: str):
    """
    Direct pyodbc connection for master DB (no pooling), for CREATE DATABASE etc.
    """
    creds = json.loads(get_db_credentials(param_name))
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={creds['host']},{creds.get('port', 1433)};"
        f"DATABASE=master;"
        f"UID={creds['username']};"
        f"PWD={creds['password']}"
    )
    return pyodbc.connect(conn_str, autocommit=True)

def _create_mssql_engine(creds) -> Engine:
    """
    SQLAlchemy engine with pooling for the actual target database.
    """
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={creds['host']},{creds.get('port', 1433)};"
        f"DATABASE={creds['database']};"
        f"UID={creds['username']};"
        f"PWD={creds['password']}"
    )
    odbc_connect = urllib.parse.quote_plus(conn_str)
    return create_engine(
        f"mssql+pyodbc:///?odbc_connect={odbc_connect}",
        pool_size=200, max_overflow=100, pool_recycle=3600
    )

def _get_mssql_target_engine(param_name: str) -> Engine:
    global _mssql_engine_target
    with _mssql_lock:
        if _mssql_engine_target is None:
            creds = json.loads(get_db_credentials(param_name))
            _mssql_engine_target = _create_mssql_engine(creds)
        return _mssql_engine_target

def get_mssqlserver_connection(param_name: str):
    return _get_mssql_target_engine(param_name).raw_connection()

# ----------------- ORACLE -----------------------
def _get_oracle_engine(param_name: str) -> Engine:
    global _oracle_engine
    with _lock:
        if _oracle_engine is None:
            creds = json.loads(get_db_credentials(param_name))
            _oracle_engine = create_engine(
                f"oracle+cx_oracle://{quote_plus(creds['username'])}:{quote_plus(creds['password'])}@{creds['host']}:{creds.get('port', 1521)}/?service_name={creds['database']}",
                pool_size=200, max_overflow=100, pool_recycle=3600
            )
        return _oracle_engine

def get_oracle_connection(param_name: str):
    return _get_oracle_engine(param_name).raw_connection()

# ----------------- IBM DB2 -----------------------
def _get_ibmdb2_engine(param_name: str) -> Engine:
    global _ibmdb2_engine
    with _lock:
        if _ibmdb2_engine is None:
            creds = json.loads(get_db_credentials(param_name))
            _ibmdb2_engine = create_engine(
                f"ibm_db_sa://{quote_plus(creds['username'])}:{quote_plus(creds['password'])}@{creds['host']}:{creds.get('port', 50000)}/{creds['database']}",
                pool_size=200, max_overflow=100, pool_recycle=3600
            )
        return _ibmdb2_engine

def get_ibm_db2_connection(param_name: str):
    return _get_ibmdb2_engine(param_name).raw_connection()

# ----------------- DynamoDB -----------------------
def get_dynamodb_resource():
    return boto3.resource('dynamodb', region_name=REGION)

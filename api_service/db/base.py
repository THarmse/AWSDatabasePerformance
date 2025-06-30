# base.py
# Theodor Harmse - University of Liverpool
# Shared utility functions for database connectivity

import json
import os
import boto3
import pymysql
import psycopg2
import psycopg2.extras
import pyodbc

REGION = os.environ.get("AWS_REGION", "eu-west-1")


def get_db_credentials(param_name: str) -> str:
    """
    Fetch credentials from AWS Systems Manager Parameter Store.
    """
    ssm = boto3.client('ssm', region_name=REGION)
    response = ssm.get_parameter(Name=param_name, WithDecryption=True)
    return response['Parameter']['Value']


def get_mysql_connection(param_name: str):
    """
    MySQL connection using PyMySQL.
    """
    creds = json.loads(get_db_credentials(param_name))
    return pymysql.connect(
        host=creds['host'],
        user=creds['username'],
        password=creds['password'],
        database=creds['database'],
        port=int(creds.get('port', 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )


def get_aurora_mysql_connection(param_name: str):
    """
    Aurora MySQL connection (same as MySQL).
    """
    return get_mysql_connection(param_name)


def get_postgresql_connection(param_name: str):
    """
    PostgreSQL connection using psycopg2.
    """
    creds = json.loads(get_db_credentials(param_name))
    return psycopg2.connect(
        host=creds['host'],
        user=creds['username'],
        password=creds['password'],
        dbname=creds['database'],
        port=int(creds.get('port', 5432)),
        cursor_factory=psycopg2.extras.RealDictCursor
    )


def get_aurora_postgresql_connection(param_name: str):
    """
    Aurora PostgreSQL connection (same as PostgreSQL).
    """
    return get_postgresql_connection(param_name)


def get_mssqlserver_connection(param_name: str):
    """
    Microsoft SQL Server connection using pyodbc.
    """
    creds = json.loads(get_db_credentials(param_name))
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={creds['host']},{creds.get('port', 1433)};"
        f"DATABASE={creds['database']};"
        f"UID={creds['username']};"
        f"PWD={creds['password']}"
    )
    return pyodbc.connect(conn_str)


def get_oracle_connection(param_name: str):
    """
    Oracle 19c connection using cx_Oracle.
    The service_name is always 'performance_db'.
    """
    import cx_Oracle
    creds = json.loads(get_db_credentials(param_name))
    dsn = cx_Oracle.makedsn(
        creds['host'],
        int(creds.get('port', 1521)),
        service_name="performance_db"
    )
    return cx_Oracle.connect(
        user=creds['username'],
        password=creds['password'],
        dsn=dsn
    )

def get_mariadb_connection(param_name: str):
    """
    MariaDB connection using PyMySQL.
    """
    return get_mysql_connection(param_name)

def get_ibm_db2_connection(param_name: str):
    """
    IBM DB2 connection using ibm_db_dbi.
    """
    import ibm_db_dbi
    creds = json.loads(get_db_credentials(param_name))
    conn_str = (
        f"DATABASE={creds['database']};"
        f"HOSTNAME={creds['host']};"
        f"PORT={int(creds.get('port', 50000))};"
        f"PROTOCOL=TCPIP;"
        f"UID={creds['username']};"
        f"PWD={creds['password']};"
    )
    return ibm_db_dbi.connect(conn_str, "", "")


def get_dynamodb_resource():
    """
    DynamoDB boto3 resource.
    """
    return boto3.resource('dynamodb', region_name=REGION)

# base.py
# Theodor Harmse - University of Liverpool
# Shared utility functions for database services

import json
import pymysql
from api_service.aws.parameter_store import get_db_credentials

def get_mysql_connection(param_name: str):
    """
    Returns a new pymysql connection using credentials pulled from
    AWS Parameter Store.
    """
    creds_json = get_db_credentials(param_name)
    creds = json.loads(creds_json)

    return pymysql.connect(
        host=creds['host'],
        user=creds['username'],
        password=creds['password'],
        database=creds['database'],
        port=int(creds.get('port', 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )

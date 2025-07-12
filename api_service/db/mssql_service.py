# mssql_service.py
# Theodor Harmse - University of Liverpool
# Implementation of Microsoft SQL Server database operations for transaction_records table

import uuid
import random
import json
from typing import Optional
from fastapi import Body
from datetime import datetime, timedelta
from api_service.db.base import (
    get_mssqlserver_connection,
    get_mssqlserver_master_connection,
    get_db_credentials
)

# Parameter Store name for SQL Server credentials
PARAM_NAME = "/Liverpool/RDS/MSSQLServer/Credentials"

# Table name
TABLE_NAME = "transaction_records"

# SQL statement to create the table if it does not exist
CREATE_TABLE_SQL = f"""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{TABLE_NAME}' AND xtype='U')
BEGIN
    CREATE TABLE {TABLE_NAME} (
        transaction_id UNIQUEIDENTIFIER PRIMARY KEY,
        user_id NVARCHAR(36),
        transaction_ts DATETIME,
        product_id NVARCHAR(36),
        quantity INT,
        unit_price DECIMAL(10,2),
        total_amount DECIMAL(12,2),
        currency NVARCHAR(3),
        payment_method NVARCHAR(20),
        status NVARCHAR(20)
    )
END
"""

async def get_connection():
    """
    Returns a new pyodbc connection using the base utility function.
    """
    return get_mssqlserver_connection(PARAM_NAME)

async def initialize_table():
    """
    Creates the database if it does not exist, then creates the transaction_records table in SQL Server if it does not exist.
    """
    creds_json = get_db_credentials(PARAM_NAME)
    creds = json.loads(creds_json)
    database_name = creds['database']

    # Use the master connection from base.py
    master_conn = get_mssqlserver_master_connection(PARAM_NAME)
    try:
        with master_conn.cursor() as cursor:
            cursor.execute(f"IF DB_ID(N'{database_name}') IS NULL CREATE DATABASE [{database_name}]")
        master_conn.commit()
    finally:
        master_conn.close()

    # connect to the target database to create the table if needed
    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_TABLE_SQL)
        conn.commit()
        return {"message": f"Database '{database_name}' and table '{TABLE_NAME}' initialized successfully in SQL Server."}
    finally:
        conn.close()

async def load_sample_data():
    """
    Calls insert_transaction() to insert 1 random record.
    """
    for _ in range(1):
        await insert_transaction(record=None)
    return {"message": "1 sample record inserted successfully into SQL Server."}

async def insert_transaction(record: Optional[dict] = Body(None)):
    """
    Inserts a new transaction record into the table.
    If no record is provided, generates a new random sample record.
    Automatically assigns a unique transaction_id.
    """
    if record is None:
        currencies = ["USD", "EUR", "GBP"]
        payment_methods = ["CreditCard", "DebitCard", "PayPal", "ApplePay"]
        statuses = ["Completed", "Pending", "Failed", "Refunded"]

        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(5.0, 100.0), 2)
        total_amount = round(quantity * unit_price, 2)

        record = {
            "user_id": f"user-{random.randint(100, 999)}",
            "transaction_ts": (datetime.utcnow() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S'),
            "product_id": f"product-{random.randint(1, 50)}",
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": total_amount,
            "currency": random.choice(currencies),
            "payment_method": random.choice(payment_methods),
            "status": random.choice(statuses)
        }

    record["transaction_id"] = str(uuid.uuid4())

    insert_sql = f"""
    INSERT INTO {TABLE_NAME} (
        transaction_id, user_id, transaction_ts, product_id,
        quantity, unit_price, total_amount, currency,
        payment_method, status
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    """

    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                insert_sql,
                (
                    record["transaction_id"],
                    record["user_id"],
                    record["transaction_ts"],
                    record["product_id"],
                    record["quantity"],
                    record["unit_price"],
                    record["total_amount"],
                    record["currency"],
                    record["payment_method"],
                    record["status"]
                )
            )
        conn.commit()
        return {
            "message": "Record inserted successfully into SQL Server.",
            "record": {k.lower(): v for k, v in record.items()}
        }
    finally:
        conn.close()

async def select_transaction():
    """
    Retrieves a single random transaction record from the table.
    Returns JSON with column names as keys (lowercase).
    """
    select_sql = f"SELECT TOP 1 * FROM {TABLE_NAME}"

    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_sql)
            row = cursor.fetchone()

            if not row:
                return {"message": "No records found in the SQL Server table."}

            columns = [col[0] for col in cursor.description]
            result = {col.lower(): val for col, val in zip(columns, row)}

            return {"record": result}
    finally:
        conn.close()

async def update_random_transaction_status():
    """
    Updates the 'status' field of one random transaction record in SQL Server.
    Selects a new random status from predefined options.
    """
    statuses = ["Completed", "Pending", "Failed", "Refunded"]
    new_status = random.choice(statuses)

    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT TOP 1 transaction_id FROM {TABLE_NAME}")
            row = cursor.fetchone()

            if not row:
                return {"message": "No records found to update in the SQL Server table."}

            columns = [col[0] for col in cursor.description]
            result = {col.lower(): val for col, val in zip(columns, row)}
            transaction_id = result["transaction_id"]

            update_sql = f"""
            UPDATE {TABLE_NAME}
            SET status = ?
            WHERE transaction_id = ?
            """
            cursor.execute(update_sql, (new_status, transaction_id))

        conn.commit()
        return {"message": f"Updated status to '{new_status}' for transaction_id {transaction_id} in SQL Server."}
    finally:
        conn.close()

async def delete_random_transaction():
    """
    Deletes one random transaction record from the SQL Server table.
    No parameters required.
    """
    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT TOP 1 transaction_id FROM {TABLE_NAME}")
            row = cursor.fetchone()

            if not row:
                return {"message": "No records found to delete in the SQL Server table."}

            columns = [col[0] for col in cursor.description]
            result = {col.lower(): val for col, val in zip(columns, row)}
            transaction_id = result["transaction_id"]

            delete_sql = f"DELETE FROM {TABLE_NAME} WHERE transaction_id = ?"
            cursor.execute(delete_sql, (transaction_id,))

        conn.commit()
        return {"message": f"Deleted transaction with ID {transaction_id} from SQL Server."}
    finally:
        conn.close()

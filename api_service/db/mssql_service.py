# mssql_service.py
# Theodor Harmse - University of Liverpool
# Implementation of Microsoft SQL Server database operations for transaction_records table

import uuid
import random
from typing import Optional
from fastapi import Body
from datetime import datetime, timedelta
from api_service.db.base import get_mssqlserver_connection

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
    Creates the transaction_records table in SQL Server if it does not exist.
    """
    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_TABLE_SQL)
        conn.commit()
        return {"message": f"Table '{TABLE_NAME}' initialized successfully in SQL Server."}
    finally:
        conn.close()

async def load_sample_data():
    """
    Calls insert_transaction() 100 times to insert 100 random records.
    """
    for _ in range(100):
        await insert_transaction(record=None)
    return {"message": "100 sample records inserted successfully into SQL Server."}

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

    # Always assign a new transaction_id
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
        return {"message": "Record inserted successfully into SQL Server.", "transaction_id": record["transaction_id"]}
    finally:
        conn.close()

async def select_transaction():
    """
    Retrieves a single random transaction record from the table.
    No parameters required.
    """
    select_sql = f"SELECT TOP 1 * FROM {TABLE_NAME} ORDER BY NEWID()"

    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_sql)
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            if row:
                result = dict(zip(columns, row))
                return {"record": result}
            else:
                return {"message": "No records found in the SQL Server table."}
    finally:
        conn.close()

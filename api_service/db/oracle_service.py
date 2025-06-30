# oracle_service.py
# Theodor Harmse - University of Liverpool
# Implementation of Oracle database operations for transaction_records table

import uuid
import random
import json
import cx_Oracle
from typing import Optional
from fastapi import Body
from datetime import datetime, timedelta
from api_service.db.base import get_oracle_connection, get_db_credentials

# Parameter Store name for Oracle credentials
PARAM_NAME = "/Liverpool/RDS/OracleDB/Credentials"

# Table name
TABLE_NAME = "transaction_records"

# PL/SQL block to create the table if it does not exist
CREATE_TABLE_PLSQL = f"""
BEGIN
  EXECUTE IMMEDIATE '
    CREATE TABLE {TABLE_NAME} (
      transaction_id VARCHAR2(36) PRIMARY KEY,
      user_id VARCHAR2(36),
      transaction_ts TIMESTAMP,
      product_id VARCHAR2(36),
      quantity NUMBER,
      unit_price NUMBER(10,2),
      total_amount NUMBER(12,2),
      currency VARCHAR2(3),
      payment_method VARCHAR2(20),
      status VARCHAR2(20)
    )';
EXCEPTION
  WHEN OTHERS THEN
    IF SQLCODE != -955 THEN
      RAISE;
    END IF;
END;
"""

async def get_connection():
    """
    Returns a new cx_Oracle connection using the base utility function.
    """
    return get_oracle_connection(PARAM_NAME)

async def initialize_table():
    """
    Creates the transaction_records table in Oracle if it does not exist.
    """
    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_TABLE_PLSQL)
        conn.commit()
        return {"message": f"Table '{TABLE_NAME}' initialized successfully in Oracle."}
    finally:
        conn.close()

async def load_sample_data():
    """
    Calls insert_transaction() 100 times to insert 100 random records.
    """
    for _ in range(100):
        await insert_transaction(record=None)
    return {"message": "100 sample records inserted successfully into Oracle."}

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
        :1, :2, :3, :4, :5, :6, :7, :8, :9, :10
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
        return {"message": "Record inserted successfully into Oracle.", "transaction_id": record["transaction_id"]}
    finally:
        conn.close()

async def select_transaction():
    """
    Retrieves a single random transaction record from the table.
    No parameters required.
    """
    select_sql = f"""
    SELECT *
    FROM (
        SELECT * FROM {TABLE_NAME} ORDER BY dbms_random.value
    ) WHERE ROWNUM = 1
    """

    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_sql)
            columns = [col[0].lower() for col in cursor.description]
            row = cursor.fetchone()
            if row:
                result = dict(zip(columns, row))
                return {"record": result}
            else:
                return {"message": "No records found in the Oracle table."}
    finally:
        conn.close()

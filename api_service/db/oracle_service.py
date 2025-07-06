# oracle_service.py
# Theodor Harmse - University of Liverpool
# Implementation of Oracle database operations for transaction_records table

import uuid
import random
from typing import Optional
from fastapi import Body
from datetime import datetime, timedelta
from api_service.db.base import get_oracle_connection

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
    Inserts 1 random sample record into the transaction_records table.
    """
    await insert_transaction(record=None)
    return {"message": "1 sample record inserted successfully into Oracle."}

async def insert_transaction(record: Optional[dict] = Body(None)):
    """
    Inserts a new transaction record into the table.
    If no record is provided, generates a random sample record.
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
            "transaction_ts": datetime.utcnow() - timedelta(days=random.randint(0, 30)),
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
        return {
            "message": "Record inserted successfully into Oracle.",
            "record": {k.lower(): v for k, v in record.items()}
        }
    finally:
        conn.close()

async def select_transaction():
    """
    Retrieves a single random transaction record from the table.
    Returns JSON with column names as lowercase keys.
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
            row = cursor.fetchone()

            if not row:
                return {"message": "No records found in the Oracle table."}

            columns = [col[0].lower() for col in cursor.description]
            result = dict(zip(columns, row))

            return {"record": result}
    finally:
        conn.close()

async def update_random_transaction_status():
    """
    Updates the 'status' field of one random transaction record in Oracle.
    Selects a new random status from predefined options.
    """
    statuses = ["Completed", "Pending", "Failed", "Refunded"]
    new_status = random.choice(statuses)

    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT transaction_id FROM (
                    SELECT transaction_id FROM {TABLE_NAME} ORDER BY dbms_random.value
                ) WHERE ROWNUM = 1
            """)
            row = cursor.fetchone()

            if not row:
                return {"message": "No records found to update in the Oracle table."}

            transaction_id = row[0]

            cursor.execute(f"""
                UPDATE {TABLE_NAME}
                SET status = :1
                WHERE transaction_id = :2
            """, (new_status, transaction_id))

        conn.commit()
        return {"message": f"Updated status to '{new_status}' for transaction_id {transaction_id} in Oracle."}
    finally:
        conn.close()

async def delete_random_transaction():
    """
    Deletes one random transaction record from the Oracle table.
    No parameters required.
    """
    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT transaction_id FROM (
                    SELECT transaction_id FROM {TABLE_NAME} ORDER BY dbms_random.value
                ) WHERE ROWNUM = 1
            """)
            row = cursor.fetchone()

            if not row:
                return {"message": "No records found to delete in the Oracle table."}

            transaction_id = row[0]

            cursor.execute(
                f"DELETE FROM {TABLE_NAME} WHERE transaction_id = :1",
                (transaction_id,)
            )

        conn.commit()
        return {"message": f"Deleted transaction with ID {transaction_id} from Oracle."}
    finally:
        conn.close()

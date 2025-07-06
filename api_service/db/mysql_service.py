# mysql_service.py
# Theodor Harmse - University of Liverpool
# Implementation of MySQL database operations for transaction_records table

import uuid
import random
from typing import Optional
from fastapi import Body
from datetime import datetime, timedelta
from api_service.db.base import get_mysql_connection 

# Parameter Store name for MySQL credentials
PARAM_NAME = "/Liverpool/RDS/MySQL/Credentials"

# Table name
TABLE_NAME = "transaction_records"

# SQL statement to create the table if it does not exist
CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    transaction_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    transaction_ts TIMESTAMP,
    product_id VARCHAR(36),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(12,2),
    currency VARCHAR(3),
    payment_method VARCHAR(20),
    status VARCHAR(20)
);
"""

async def get_connection():
    """
    Returns a new pymysql connection using the base utility function.
    Centralizes Parameter Store access and JSON parsing in base.py.
    """
    return get_mysql_connection(PARAM_NAME)

async def initialize_table():
    """
    Creates the transaction_records table if it does not exist.
    """
    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_TABLE_SQL)
        conn.commit()
        return {"message": f"Table '{TABLE_NAME}' initialized successfully."}
    finally:
        conn.close()

async def load_sample_data():
    """
    Calls insert_transaction() to insert 1 random record.
    """
    for _ in range(1):
        await insert_transaction(record=None)
    return {"message": "1 sample record inserted successfully."}

async def insert_transaction(record: Optional[dict] = Body(None)):
    """
    Inserts a new transaction record into the table.
    If no record is provided, generates a new random sample record.
    Automatically assigns a unique transaction_id.
    """
    if record is None:
        # Generate a random sample record
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
        %(transaction_id)s, %(user_id)s, %(transaction_ts)s, %(product_id)s,
        %(quantity)s, %(unit_price)s, %(total_amount)s, %(currency)s,
        %(payment_method)s, %(status)s
    )
    """

    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(insert_sql, record)
        conn.commit()
        return {
            "message": "Record inserted successfully.",
            "record": {k.lower(): v for k, v in record.items()}
        }
    finally:
        conn.close()

async def select_transaction():
    """
    Retrieves a single random transaction record from the table.
    No parameters required.
    Returns a JSON object with column names as keys (lowercase).
    """
    select_sql = f"SELECT * FROM {TABLE_NAME} ORDER BY RAND() LIMIT 1"

    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_sql)
            row = cursor.fetchone()

            if not row:
                return {"message": "No records found in the table."}

            # Extract columns and zip into a dict with lowercase keys
            columns = [col[0] for col in cursor.description]
            result = {col.lower(): val for col, val in zip(columns, row)}

            return {"record": result}
    finally:
        conn.close()

async def update_random_transaction_status():
    """
    Updates the 'status' field of one random transaction record.
    Chooses a new random status from predefined options.
    """
    statuses = ["Completed", "Pending", "Failed", "Refunded"]
    new_status = random.choice(statuses)

    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            # Get a random transaction_id
            cursor.execute(f"SELECT transaction_id FROM {TABLE_NAME} ORDER BY RAND() LIMIT 1")
            row = cursor.fetchone()

            if not row:
                return {"message": "No records found to update."}

            columns = [col[0] for col in cursor.description]
            result = {col.lower(): val for col, val in zip(columns, row)}
            transaction_id = result["transaction_id"]

            # Update the status
            update_sql = f"""
            UPDATE {TABLE_NAME}
            SET status = %s
            WHERE transaction_id = %s
            """
            cursor.execute(update_sql, (new_status, transaction_id))

        conn.commit()
        return {"message": f"Updated status to '{new_status}' for transaction_id {transaction_id}."}
    finally:
        conn.close()

async def delete_random_transaction():
    """
    Deletes one random transaction record from the table.
    No parameters required.
    """
    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            # Get a random transaction_id
            cursor.execute(f"SELECT transaction_id FROM {TABLE_NAME} ORDER BY RAND() LIMIT 1")
            row = cursor.fetchone()

            if not row:
                return {"message": "No records found to delete."}

            columns = [col[0] for col in cursor.description]
            result = {col.lower(): val for col, val in zip(columns, row)}
            transaction_id = result["transaction_id"]

            # Delete the record
            delete_sql = f"DELETE FROM {TABLE_NAME} WHERE transaction_id = %s"
            cursor.execute(delete_sql, (transaction_id,))

        conn.commit()
        return {"message": f"Deleted transaction with ID {transaction_id}."}
    finally:
        conn.close()

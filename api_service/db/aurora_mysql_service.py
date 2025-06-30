# aurora_mysql_service.py
# Theodor Harmse - University of Liverpool
# Implementation of Aurora MySQL database operations for transaction_records table

import uuid
import random
from typing import Optional
from fastapi import Body
from datetime import datetime, timedelta
from api_service.db.base import get_aurora_mysql_connection

# Parameter Store name for Aurora MySQL credentials
PARAM_NAME = "/Liverpool/RDS/AuroraMySQL/Credentials"

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
    Returns a new pymysql connection to Aurora MySQL using the shared base utility.
    """
    return get_aurora_mysql_connection(PARAM_NAME)

async def initialize_table():
    """
    Creates the transaction_records table in Aurora MySQL if it does not exist.
    """
    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_TABLE_SQL)
        conn.commit()
        return {"message": f"Table '{TABLE_NAME}' initialized successfully in Aurora MySQL."}
    finally:
        conn.close()

async def load_sample_data():
    """
    Inserts 100 random sample records into the transaction_records table.
    """
    for _ in range(100):
        await insert_transaction(record=None)
    return {"message": "100 sample records inserted successfully into Aurora MySQL."}

async def insert_transaction(record: Optional[dict] = Body(None)):
    """
    Inserts a new transaction record into the Aurora MySQL table.
    Generates a random sample record if none is provided.
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
        return {"message": "Record inserted successfully into Aurora MySQL.", "transaction_id": record["transaction_id"]}
    finally:
        conn.close()

async def select_transaction():
    """
    Retrieves a single random transaction record from the Aurora MySQL table.
    """
    select_sql = f"SELECT * FROM {TABLE_NAME} ORDER BY RAND() LIMIT 1"

    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_sql)
            result = cursor.fetchone()
        if result:
            return {"record": result}
        else:
            return {"message": "No records found in the Aurora MySQL table."}
    finally:
        conn.close()

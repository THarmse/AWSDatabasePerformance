# ibmdb2_service.py
# Theodor Harmse - University of Liverpool
# Implementation of IBM Db2 database operations for transaction_records table

import uuid
import random
import json
import ibm_db_dbi
from typing import Optional
from fastapi import Body
from datetime import datetime, timedelta
from api_service.db.base import get_ibm_db2_connection, get_db_credentials

# Parameter Store name for IBM Db2 credentials
PARAM_NAME = "/Liverpool/RDS/IBMDB2/Credentials"

# Table name
TABLE_NAME = "transaction_records"

# SQL to create the table if it does not exist
CREATE_TABLE_SQL = f"""
BEGIN
  DECLARE CONTINUE HANDLER FOR SQLSTATE '42710' BEGIN END;
  EXECUTE IMMEDIATE '
    CREATE TABLE {TABLE_NAME} (
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
    )';
END
"""

async def get_connection():
    """
    Returns a new ibm_db_dbi connection using the base utility function.
    """
    return get_ibm_db2_connection(PARAM_NAME)


async def initialize_table():
    """
    Creates the transaction_records table if it does not already exist.
    """
    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_TABLE_SQL)
        conn.commit()
        return {"message": f"Table '{TABLE_NAME}' initialized successfully in IBM Db2."}
    finally:
        conn.close()



async def load_sample_data():
    """
    Calls insert_transaction() to insert 1 random record.
    """
    await insert_transaction(record=None)
    return {"message": "1 sample record inserted successfully into IBM Db2."}


async def insert_transaction(record: Optional[dict] = Body(None)):
    """
    Inserts a new transaction record into the table.
    If no record is provided, generates a new random sample record.
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
        return {"message": "Record inserted successfully into IBM Db2.", "transaction_id": record["transaction_id"]}
    finally:
        conn.close()


async def select_transaction():
    """
    Retrieves a single random transaction record from the table.
    """
    select_sql = f"SELECT * FROM {TABLE_NAME} ORDER BY RAND() FETCH FIRST 1 ROW ONLY"

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
                return {"message": "No records found in the IBM Db2 table."}
    finally:
        conn.close()


async def update_random_transaction_status():
    """
    Updates the 'status' field of one random transaction record in IBM Db2.
    """
    statuses = ["Completed", "Pending", "Failed", "Refunded"]
    new_status = random.choice(statuses)

    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            # Retrieve a random transaction_id
            cursor.execute(f"SELECT transaction_id FROM {TABLE_NAME} ORDER BY RAND() FETCH FIRST 1 ROW ONLY")
            result = cursor.fetchone()

            if not result:
                return {"message": "No records found to update in the IBM Db2 table."}

            transaction_id = result[0]

            # Perform the update
            update_sql = f"""
            UPDATE {TABLE_NAME}
            SET status = ?
            WHERE transaction_id = ?
            """
            cursor.execute(update_sql, (new_status, transaction_id))

        conn.commit()
        return {"message": f"Updated status to '{new_status}' for transaction_id {transaction_id} in IBM Db2."}
    finally:
        conn.close()


async def delete_random_transaction():
    """
    Deletes one random transaction record from the IBM Db2 table.
    """
    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            # Retrieve a random transaction_id
            cursor.execute(f"SELECT transaction_id FROM {TABLE_NAME} ORDER BY RAND() FETCH FIRST 1 ROW ONLY")
            result = cursor.fetchone()

            if not result:
                return {"message": "No records found to delete in the IBM Db2 table."}

            transaction_id = result[0]

            # Perform the deletion
            delete_sql = f"DELETE FROM {TABLE_NAME} WHERE transaction_id = ?"
            cursor.execute(delete_sql, (transaction_id,))

        conn.commit()
        return {"message": f"Deleted transaction with ID {transaction_id} from IBM Db2."}
    finally:
        conn.close()

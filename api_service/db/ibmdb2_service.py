# ibmdb2_service.py
# Theodor Harmse - University of Liverpool
# Implementation of IBM Db2 database operations for transaction_records table

import uuid
import random
import ibm_db_dbi
from typing import Optional
from fastapi import Body
from datetime import datetime, timedelta
from api_service.db.base import get_ibm_db2_connection

# Parameter Store name for IBM Db2 credentials
PARAM_NAME = "/Liverpool/RDS/IBMDB2/Credentials"

# Table name
TABLE_NAME = "transaction_records"


async def get_connection(autocommit: bool = True):
    """
    Returns a new ibm_db_dbi connection using the base utility function.
    By default, enables autocommit for stateless REST interactions.
    """
    conn = get_ibm_db2_connection(PARAM_NAME)
    conn.autocommit = autocommit
    return conn


async def initialize_table():
    """
    Ensures the ADMINUSER schema exists, and creates the transaction_records table if it does not already exist.
    """
    conn = await get_connection(autocommit=True)
    try:
        with conn.cursor() as cursor:
            # Determine the current schema (matches connected user)
            cursor.execute("VALUES CURRENT SCHEMA")
            schema = cursor.fetchone()[0].strip().upper()
            print(f"[INFO] Current schema: {schema}")

            # Check if the schema exists
            cursor.execute("""
                SELECT 1 FROM SYSCAT.SCHEMATA WHERE SCHEMANAME = ?
            """, (schema,))
            if not cursor.fetchone():
                print(f"[INFO] Schema '{schema}' does not exist. Creating it.")
                cursor.execute(f"CREATE SCHEMA {schema}")
                print(f"[INFO] Schema '{schema}' created successfully.")

            # Check if the table already exists in the schema
            cursor.execute("""
                SELECT 1 FROM SYSCAT.TABLES
                WHERE TABNAME = ? AND TABSCHEMA = ?
            """, (TABLE_NAME.upper(), schema))
            if cursor.fetchone():
                print(f"[INFO] Table '{TABLE_NAME}' already exists in schema '{schema}'.")
                return {"message": f"Table '{TABLE_NAME}' already exists in IBM Db2."}

            # Table does not exist - create it
            create_table_sql = f"""
            CREATE TABLE {schema}.{TABLE_NAME} (
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
            )
            """
            print(f"[INFO] Creating table with SQL:\n{create_table_sql}")
            cursor.execute(create_table_sql)
            print(f"[INFO] Table '{TABLE_NAME}' created successfully in schema '{schema}'.")

        return {"message": f"Table '{TABLE_NAME}' created successfully in IBM Db2."}

    except Exception as e:
        print(f"[ERROR] Exception during initialize_table: {e}")
        return {"error": str(e)}

    finally:
        try:
            conn.close()
            print("[INFO] Connection closed.")
        except Exception as close_error:
            print(f"[WARN] Exception during connection close: {close_error}")






async def load_sample_data():
    """
    Inserts one random sample record into the transaction_records table.
    """
    await insert_transaction(record=None)
    return {"message": "1 sample record inserted successfully into IBM Db2."}


async def insert_transaction(record: Optional[dict] = Body(None)):
    """
    Inserts a new transaction record into the table.
    Generates a random sample record if none is provided.
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
        return {"message": "Record inserted successfully into IBM Db2.", "transaction_id": record["transaction_id"]}
    finally:
        conn.close()


async def select_transaction():
    """
    Retrieves a single transaction record from the table.
    """
    select_sql = f"SELECT * FROM {TABLE_NAME} FETCH FIRST 1 ROW ONLY"

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
    Updates the 'status' field of one transaction record in IBM Db2.
    """
    statuses = ["Completed", "Pending", "Failed", "Refunded"]
    new_status = random.choice(statuses)

    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT transaction_id FROM {TABLE_NAME} FETCH FIRST 1 ROW ONLY")
            result = cursor.fetchone()

            if not result or result[0] is None:
                return {"message": "No records found to update in the IBM Db2 table."}

            transaction_id = result[0]

            update_sql = f"""
            UPDATE {TABLE_NAME}
            SET status = ?
            WHERE transaction_id = ?
            """
            cursor.execute(update_sql, (new_status, transaction_id))

        return {"message": f"Updated status to '{new_status}' for transaction_id {transaction_id} in IBM Db2."}
    finally:
        conn.close()


async def delete_random_transaction():
    """
    Deletes one transaction record from the IBM Db2 table.
    """
    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT transaction_id FROM {TABLE_NAME} FETCH FIRST 1 ROW ONLY")
            result = cursor.fetchone()

            if not result or result[0] is None:
                return {"message": "No records found to delete in the IBM Db2 table."}

            transaction_id = result[0]

            delete_sql = f"DELETE FROM {TABLE_NAME} WHERE transaction_id = ?"
            cursor.execute(delete_sql, (transaction_id,))

        return {"message": f"Deleted transaction with ID {transaction_id} from IBM Db2."}
    finally:
        conn.close()

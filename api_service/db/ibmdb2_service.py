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
    Ensures both the schema and the transaction_records table exist in IBM Db2.
    Creates schema and grants privileges if needed. Fully idempotent.
    Prints extra info for troubleshooting.
    """
    conn = await get_connection(autocommit=True)
    try:
        with conn.cursor() as cursor:
            # Get session details for troubleshooting
            cursor.execute("VALUES SESSION_USER")
            session_user = cursor.fetchone()[0].strip().upper()

            cursor.execute("VALUES CURRENT SCHEMA")
            current_schema = cursor.fetchone()[0].strip().upper()

            cursor.execute("VALUES CURRENT SERVER")
            current_server = cursor.fetchone()[0].strip().upper()

            print(f"[INFO] Connected to DB2:")
            print(f"  - Host (DB alias): {current_server}")
            print(f"  - Session User: {session_user}")
            print(f"  - Current Schema: {current_schema}")

            schema = session_user

            # Check if the schema exists
            print(f"[INFO] Checking if schema '{schema}' exists...")
            cursor.execute(
                "SELECT 1 FROM SYSCAT.SCHEMATA WHERE SCHEMANAME = ?",
                (schema,)
            )
            if not cursor.fetchone():
                # Confirm user exists in DB2 catalog
                print(f"[INFO] Schema '{schema}' does not exist. Checking if user '{schema}' exists...")
                cursor.execute(
                    "SELECT 1 FROM SYSIBM.SYSUSERAUTH WHERE AUTHID = ?",
                    (schema,)
                )
                if cursor.fetchone():
                    print(f"[INFO] User '{schema}' exists. Attempting to create schema...")
                    try:
                        cursor.execute(f"CREATE SCHEMA {schema} AUTHORIZATION {schema}")
                        print(f"[INFO] Schema '{schema}' created successfully.")
                    except Exception as e:
                        print(f"[WARN] Could not create schema '{schema}': {e}")
                else:
                    print(f"[ERROR] User '{schema}' does not exist in DB2. Cannot create schema.")
                    return {"error": f"User '{schema}' does not exist in DB2. Please create the user first."}

            # Check CREATEIN privilege
            print(f"[INFO] Checking CREATEIN privilege for '{schema}' on schema '{schema}'...")
            cursor.execute("""
                SELECT DB2AUTH FROM SYSCAT.SCHEMAAUTH
                WHERE SCHEMANAME = ? AND GRANTEE = ?
            """, (schema, schema))
            privs = [row[0] for row in cursor.fetchall()]
            print(f"[INFO] Found privileges: {privs}")

            if 'C' not in privs:
                print(f"[INFO] User '{schema}' lacks CREATEIN. Attempting to grant...")
                try:
                    cursor.execute(f"GRANT CREATEIN ON SCHEMA {schema} TO USER {schema}")
                    print(f"[INFO] Granted CREATEIN on schema '{schema}' to user '{schema}'.")
                except Exception as e:
                    print(f"[WARN] Could not grant CREATEIN on schema '{schema}' to user '{schema}': {e}")

            # Check if the table exists
            print(f"[INFO] Checking if table '{TABLE_NAME}' exists in schema '{schema}'...")
            cursor.execute("""
                SELECT 1 FROM SYSCAT.TABLES
                WHERE TABNAME = ? AND TABSCHEMA = ?
            """, (TABLE_NAME.upper(), schema))
            if cursor.fetchone():
                print(f"[INFO] Table '{TABLE_NAME}' already exists in schema '{schema}'.")
                return {"message": f"Table '{TABLE_NAME}' already exists in IBM Db2."}

            # Create the table
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
            print(f"[INFO] Executing CREATE TABLE:\n{create_table_sql}")
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

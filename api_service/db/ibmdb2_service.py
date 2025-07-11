# ibmdb2_service.py
# Theodor Harmse - University of Liverpool
# Implementation of IBM Db2 database operations for transaction_records table

import uuid
import random
from typing import Optional
from fastapi import Body
from datetime import datetime, timedelta
from api_service.db.base import get_ibm_db2_connection

# Parameter Store name for IBM Db2 credentials
PARAM_NAME = "/Liverpool/RDS/IBMDB2/Credentials"
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
    Ensures the connected user's schema exists, and creates the transaction_records table if it does not already exist.
    Designed to be idempotent and safe to run multiple times.
    """
    conn = await get_connection(autocommit=False)
    try:
        with conn.cursor() as cursor:
            cursor.execute("VALUES CURRENT SCHEMA")
            schema = cursor.fetchone()[0].strip().upper()

            cursor.execute("""
                SELECT 1 FROM SYSCAT.SCHEMATA WHERE SCHEMANAME = ?
            """, (schema,))
            if not cursor.fetchone():
                cursor.execute(f"CREATE SCHEMA {schema}")
                conn.commit()

            cursor.execute("""
                SELECT 1 FROM SYSCAT.TABLES
                WHERE TABNAME = ? AND TABSCHEMA = ?
            """, (TABLE_NAME.upper(), schema))
            if cursor.fetchone():
                return {"message": f"Table '{TABLE_NAME}' already exists in IBM Db2."}

            create_table_sql = f"""
            CREATE TABLE {schema}.{TABLE_NAME} (
                transaction_id VARCHAR(36) NOT NULL PRIMARY KEY,
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
            cursor.execute(create_table_sql)
            conn.commit()

        return {"message": f"Table '{TABLE_NAME}' created successfully in IBM Db2."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()


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

    conn = await get_connection(autocommit=False)
    try:
        with conn.cursor() as cursor:
            cursor.execute("VALUES CURRENT SCHEMA")
            schema = cursor.fetchone()[0].strip().upper()

            insert_sql = f"""
            INSERT INTO {schema}.{TABLE_NAME} (
                transaction_id, user_id, transaction_ts, product_id,
                quantity, unit_price, total_amount, currency,
                payment_method, status
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """
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
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()


async def select_transaction():
    """
    Retrieves a single transaction record from the table.
    """
    conn = await get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("VALUES CURRENT SCHEMA")
            schema = cursor.fetchone()[0].strip().upper()

            select_sql = f"SELECT * FROM {schema}.{TABLE_NAME} FETCH FIRST 1 ROW ONLY"
            cursor.execute(select_sql)
            row = cursor.fetchone()

            if not row:
                return {"message": "No records found in the IBM Db2 table."}

            columns = [column[0].lower() for column in cursor.description]
            result = dict(zip(columns, row))

            return {"record": result}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()


async def update_random_transaction_status():
    """
    Updates the 'status' field of one transaction record in IBM Db2.
    """
    statuses = ["Completed", "Pending", "Failed", "Refunded"]
    new_status = random.choice(statuses)

    conn = await get_connection(autocommit=False)
    try:
        with conn.cursor() as cursor:
            cursor.execute("VALUES CURRENT SCHEMA")
            schema = cursor.fetchone()[0].strip().upper()

            cursor.execute(f"SELECT transaction_id FROM {schema}.{TABLE_NAME} FETCH FIRST 1 ROW ONLY")
            row = cursor.fetchone()

            if not row or not row[0]:
                return {"message": "No records found to update in the IBM Db2 table."}

            transaction_id = row[0]

            update_sql = f"""
            UPDATE {schema}.{TABLE_NAME}
            SET status = ?
            WHERE transaction_id = ?
            """
            cursor.execute(update_sql, (new_status, transaction_id))
            conn.commit()

        return {"message": f"Updated status to '{new_status}' for transaction_id {transaction_id} in IBM Db2."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()


async def delete_random_transaction():
    """
    Deletes one transaction record from the IBM Db2 table.
    """
    conn = await get_connection(autocommit=False)
    try:
        with conn.cursor() as cursor:
            cursor.execute("VALUES CURRENT SCHEMA")
            schema = cursor.fetchone()[0].strip().upper()

            cursor.execute(f"SELECT transaction_id FROM {schema}.{TABLE_NAME} FETCH FIRST 1 ROW ONLY")
            row = cursor.fetchone()

            if not row or not row[0]:
                return {"message": "No records found to delete in the IBM Db2 table."}

            transaction_id = row[0]

            delete_sql = f"DELETE FROM {schema}.{TABLE_NAME} WHERE transaction_id = ?"
            cursor.execute(delete_sql, (transaction_id,))
            conn.commit()

        return {"message": f"Deleted transaction with ID {transaction_id} from IBM Db2."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

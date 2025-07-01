# main.py
# Theodor Harmse - University of Liverpool
# FastAPI app exposing MySQL and Aurora MySQL transaction_records service endpoints

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Import MySQL service functions
from api_service.db.mysql_service import (
    initialize_table as mysql_initialize_table,
    load_sample_data as mysql_load_sample_data,
    select_transaction as mysql_select_transaction,
    insert_transaction as mysql_insert_transaction,
    update_random_transaction_status as mysql_update_random_transaction_status,
    delete_random_transaction as mysql_delete_random_transaction
)

# Import Aurora MySQL service functions
from api_service.db.aurora_mysql_service import (
    initialize_table as aurora_initialize_table,
    load_sample_data as aurora_load_sample_data,
    select_transaction as aurora_select_transaction,
    insert_transaction as aurora_insert_transaction
)

# Import PostgreSQL service functions
from api_service.db.postgresql_service import (
    initialize_table as postgresql_initialize_table,
    load_sample_data as postgresql_load_sample_data,
    select_transaction as postgresql_select_transaction,
    insert_transaction as postgresql_insert_transaction
)

# Import Aurora PostgreSQL service functions
from api_service.db.aurora_postgresql_service import (
    initialize_table as aurora_postgresql_initialize_table,
    load_sample_data as aurora_postgresql_load_sample_data,
    select_transaction as aurora_postgresql_select_transaction,
    insert_transaction as aurora_postgresql_insert_transaction
)

# Import MariaDB service functions
from api_service.db.mariadb_service import (
    initialize_table as mariadb_initialize_table,
    load_sample_data as mariadb_load_sample_data,
    select_transaction as mariadb_select_transaction,
    insert_transaction as mariadb_insert_transaction
)

# Import Microsoft SQL Server service functions
from api_service.db.mssql_service import (
    initialize_table as mssql_initialize_table,
    load_sample_data as mssql_load_sample_data,
    select_transaction as mssql_select_transaction,
    insert_transaction as mssql_insert_transaction
)

# Import Oracle service functions
from api_service.db.oracle_service import (
    initialize_table as oracle_initialize_table,
    load_sample_data as oracle_load_sample_data,
    select_transaction as oracle_select_transaction,
    insert_transaction as oracle_insert_transaction
)

# Import DynamoDB service functions
from api_service.db.dynamodb_service import (
    initialize_table as dynamodb_initialize_table,
    load_sample_data as dynamodb_load_sample_data,
    select_transaction as dynamodb_select_transaction,
    insert_transaction as dynamodb_insert_transaction
)




# Define FastAPI app
app = FastAPI(
    title="University of Liverpool - Transaction Records API",
    description="API service for managing transaction_records table on both MySQL and Aurora MySQL RDS instances.",
    version="1.0.0"
)

# Pydantic model for insert request body
class TransactionRecord(BaseModel):
    user_id: str
    transaction_ts: str
    product_id: str
    quantity: int
    unit_price: float
    total_amount: float
    currency: str
    payment_method: str
    status: str

# -------------------------
# MySQL Endpoints
# -------------------------

@app.get("/mysql/initialize")
async def api_mysql_initialize_table():
    """
    Initialize the transaction_records table in MySQL.
    """
    try:
        result = await mysql_initialize_table()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mysql/load-sample-data")
async def api_mysql_load_sample_data():
    """
    Insert 20 randomly generated sample records into the MySQL table.
    """
    try:
        result = await mysql_load_sample_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mysql/select-random")
async def api_mysql_select_random_transaction():
    """
    Retrieve one random transaction record from the MySQL table.
    """
    try:
        result = await mysql_select_transaction()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mysql/insert")
async def api_mysql_insert_transaction(record: TransactionRecord):
    """
    Insert a new transaction record into MySQL.
    transaction_id is generated automatically.
    """
    try:
        result = await mysql_insert_transaction(record.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mysql/update-random-status")
async def api_mysql_update_random_status():
    """
    Update the 'status' field of one random transaction record in MySQL.
    No parameters required.
    """
    try:
        result = await mysql_update_random_transaction_status()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/mysql/delete-random")
async def api_mysql_delete_random_transaction():
    """
    Delete one random transaction record from the MySQL table.
    No parameters required.
    """
    try:
        result = await mysql_delete_random_transaction()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# Aurora MySQL Endpoints
# -------------------------

@app.get("/AuroraMySQL/initialize")
async def api_aurora_initialize_table():
    """
    Initialize the transaction_records table in Aurora MySQL.
    """
    try:
        result = await aurora_initialize_table()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/AuroraMySQL/load-sample-data")
async def api_aurora_load_sample_data():
    """
    Insert 20 randomly generated sample records into the Aurora MySQL table.
    """
    try:
        result = await aurora_load_sample_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/AuroraMySQL/select-random")
async def api_aurora_select_random_transaction():
    """
    Retrieve one random transaction record from the Aurora MySQL table.
    """
    try:
        result = await aurora_select_transaction()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/AuroraMySQL/insert")
async def api_aurora_insert_transaction(record: TransactionRecord):
    """
    Insert a new transaction record into Aurora MySQL.
    transaction_id is generated automatically.
    """
    try:
        result = await aurora_insert_transaction(record.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# PostgreSQL Endpoints
# -------------------------

@app.get("/postgresql/initialize")
async def api_postgresql_initialize_table():
    """
    Initialize the transaction_records table in PostgreSQL.
    """
    try:
        result = await postgresql_initialize_table()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/postgresql/load-sample-data")
async def api_postgresql_load_sample_data():
    """
    Insert 100 randomly generated sample records into the PostgreSQL table.
    """
    try:
        result = await postgresql_load_sample_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/postgresql/select-random")
async def api_postgresql_select_random_transaction():
    """
    Retrieve one random transaction record from the PostgreSQL table.
    """
    try:
        result = await postgresql_select_transaction()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/postgresql/insert")
async def api_postgresql_insert_transaction(record: TransactionRecord):
    """
    Insert a new transaction record into PostgreSQL.
    transaction_id is generated automatically.
    """
    try:
        result = await postgresql_insert_transaction(record.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# Aurora PostgreSQL Endpoints
# -------------------------

@app.get("/AuroraPostgreSQL/initialize")
async def api_aurora_postgresql_initialize_table():
    """
    Initialize the transaction_records table in Aurora PostgreSQL.
    """
    try:
        result = await aurora_postgresql_initialize_table()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/AuroraPostgreSQL/load-sample-data")
async def api_aurora_postgresql_load_sample_data():
    """
    Insert 100 randomly generated sample records into the Aurora PostgreSQL table.
    """
    try:
        result = await aurora_postgresql_load_sample_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/AuroraPostgreSQL/select-random")
async def api_aurora_postgresql_select_random_transaction():
    """
    Retrieve one random transaction record from the Aurora PostgreSQL table.
    """
    try:
        result = await aurora_postgresql_select_transaction()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/AuroraPostgreSQL/insert")
async def api_aurora_postgresql_insert_transaction(record: TransactionRecord):
    """
    Insert a new transaction record into Aurora PostgreSQL.
    transaction_id is generated automatically.
    """
    try:
        result = await aurora_postgresql_insert_transaction(record.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# MariaDB Endpoints
# -------------------------

@app.get("/mariadb/initialize")
async def api_mariadb_initialize_table():
    """
    Initialize the transaction_records table in MariaDB.
    """
    try:
        result = await mariadb_initialize_table()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mariadb/load-sample-data")
async def api_mariadb_load_sample_data():
    """
    Insert 100 randomly generated sample records into the MariaDB table.
    """
    try:
        result = await mariadb_load_sample_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mariadb/select-random")
async def api_mariadb_select_random_transaction():
    """
    Retrieve one random transaction record from the MariaDB table.
    """
    try:
        result = await mariadb_select_transaction()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mariadb/insert")
async def api_mariadb_insert_transaction(record: TransactionRecord):
    """
    Insert a new transaction record into MariaDB.
    transaction_id is generated automatically.
    """
    try:
        result = await mariadb_insert_transaction(record.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# Microsoft SQL Server Endpoints
# -------------------------

@app.get("/mssql/initialize")
async def api_mssql_initialize_table():
    """
    Initialize the transaction_records table in Microsoft SQL Server.
    """
    try:
        result = await mssql_initialize_table()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mssql/load-sample-data")
async def api_mssql_load_sample_data():
    """
    Insert 100 randomly generated sample records into the Microsoft SQL Server table.
    """
    try:
        result = await mssql_load_sample_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mssql/select-random")
async def api_mssql_select_random_transaction():
    """
    Retrieve one random transaction record from the Microsoft SQL Server table.
    """
    try:
        result = await mssql_select_transaction()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mssql/insert")
async def api_mssql_insert_transaction(record: TransactionRecord):
    """
    Insert a new transaction record into Microsoft SQL Server.
    transaction_id is generated automatically.
    """
    try:
        result = await mssql_insert_transaction(record.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# Oracle Endpoints
# -------------------------

@app.get("/oracle/initialize")
async def api_oracle_initialize_table():
    """
    Initialize the transaction_records table in Oracle.
    """
    try:
        result = await oracle_initialize_table()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/oracle/load-sample-data")
async def api_oracle_load_sample_data():
    """
    Insert 100 randomly generated sample records into the Oracle table.
    """
    try:
        result = await oracle_load_sample_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/oracle/select-random")
async def api_oracle_select_random_transaction():
    """
    Retrieve one random transaction record from the Oracle table.
    """
    try:
        result = await oracle_select_transaction()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/oracle/insert")
async def api_oracle_insert_transaction(record: TransactionRecord):
    """
    Insert a new transaction record into Oracle.
    transaction_id is generated automatically.
    """
    try:
        result = await oracle_insert_transaction(record.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# DynamoDB Endpoints
# -------------------------

@app.get("/dynamodb/initialize")
async def api_dynamodb_initialize_table():
    """
    Initialize the transaction_records table in DynamoDB.
    """
    try:
        result = await dynamodb_initialize_table()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/dynamodb/load-sample-data")
async def api_dynamodb_load_sample_data():
    """
    Insert 100 randomly generated sample records into the DynamoDB table.
    """
    try:
        result = await dynamodb_load_sample_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dynamodb/select-random")
async def api_dynamodb_select_random_transaction():
    """
    Retrieve one random transaction record from the DynamoDB table.
    """
    try:
        result = await dynamodb_select_transaction()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/dynamodb/insert")
async def api_dynamodb_insert_transaction(record: TransactionRecord):
    """
    Insert a new transaction record into DynamoDB.
    transaction_id is generated automatically.
    """
    try:
        result = await dynamodb_insert_transaction(record.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

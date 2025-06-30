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
    insert_transaction as mysql_insert_transaction
)

# Import Aurora MySQL service functions
from api_service.db.aurora_mysql_service import (
    initialize_table as aurora_initialize_table,
    load_sample_data as aurora_load_sample_data,
    select_transaction as aurora_select_transaction,
    insert_transaction as aurora_insert_transaction
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


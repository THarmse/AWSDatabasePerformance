# main.py
# Theodor Harmse - University of Liverpool
# FastAPI app exposing MySQL transaction_records service endpoints

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from mysql_service import (
    initialize_table,
    load_sample_data,
    select_transaction,
    insert_transaction
)

# Define FastAPI app
app = FastAPI(
    title="University of Liverpool - MySQL Transaction Records API",
    description="API service for managing transaction_records table on MySQL RDS instance.",
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


@app.get("/mysql/initialize")
async def api_initialize_table():
    """
    Initialize the transaction_records table.
    Creates the table if it does not exist.
    """
    try:
        result = await initialize_table()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mysql/load-sample-data")
async def api_load_sample_data():
    """
    Insert 20 randomly generated sample records into the table.
    """
    try:
        result = await load_sample_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mysql/select-random")
async def api_select_random_transaction():
    """
    Retrieve one random transaction record from the table.
    No parameters required.
    """
    try:
        result = await select_transaction()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mysql/insert")
async def api_insert_transaction(record: TransactionRecord):
    """
    Insert a new transaction record.
    transaction_id is generated automatically.
    """
    try:
        result = await insert_transaction(record.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

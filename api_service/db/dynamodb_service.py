# dynamodb_service.py
# Theodor Harmse - University of Liverpool
# Implementation of DynamoDB operations for transaction_records table

import uuid
import random
import json
from typing import Optional
from fastapi import Body
from datetime import datetime, timedelta
import boto3
from decimal import Decimal
from botocore.exceptions import ClientError
from api_service.db.base import get_db_credentials

# Parameter Store name for DynamoDB credentials
PARAM_NAME = "/Liverpool/DynamoDB/Credentials"

async def get_table():
    """
    Returns a boto3 Table resource using credentials from Parameter Store.
    """
    creds = json.loads(get_db_credentials(PARAM_NAME))
    session = boto3.Session(region_name=creds["region"])
    dynamodb = session.resource(
        "dynamodb",
        endpoint_url=creds.get("endpoint")
    )
    return dynamodb.Table(creds["table_name"])

async def initialize_table():
    """
    Checks if the table exists. If not, creates it.
    """
    creds = json.loads(get_db_credentials(PARAM_NAME))
    session = boto3.Session(region_name=creds["region"])
    dynamodb = session.resource(
        "dynamodb",
        endpoint_url=creds.get("endpoint")
    )
    table_name = creds["table_name"]

    try:
        table = dynamodb.Table(table_name)
        table.load()
        return {"message": f"Table '{table_name}' already exists in DynamoDB."}
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceNotFoundException':
            raise
        # Create the table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'transaction_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'transaction_id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()
        return {"message": f"Table '{table_name}' created successfully in DynamoDB."}

async def load_sample_data():
    """
    Calls insert_transaction() 100 times to insert 100 random records.
    """
    for _ in range(100):
        await insert_transaction(record=None)
    return {"message": "100 sample records inserted successfully into DynamoDB."}

async def insert_transaction(record: Optional[dict] = Body(None)):
    """
    Inserts a new transaction record into the table.
    If no record is provided, generates a new random sample record.
    Automatically assigns a unique transaction_id.
    """
    if record is None:
        currencies = ["USD", "EUR", "GBP"]
        payment_methods = ["CreditCard", "DebitCard", "PayPal", "ApplePay"]
        statuses = ["Completed", "Pending", "Failed", "Refunded"]

        quantity = random.randint(1, 5)
        unit_price = Decimal(str(round(random.uniform(5.0, 100.0), 2)))
        total_amount = Decimal(str(round(quantity * unit_price, 2)))


        record = {
            "user_id": f"user-{random.randint(100, 999)}",
            "transaction_ts": (datetime.utcnow() - timedelta(days=random.randint(0, 30))).isoformat(),
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

    table = await get_table()
    table.put_item(Item=record)
    return {"message": "Record inserted successfully into DynamoDB.", "transaction_id": record["transaction_id"]}

async def select_transaction():
    """
    Retrieves one random transaction record from the DynamoDB table.
    """
    table = await get_table()
    scan_response = table.scan(Limit=10)  # Fetch up to 10 items to choose randomly

    items = scan_response.get("Items", [])
    if not items:
        return {"message": "No records found in the DynamoDB table."}

    selected = random.choice(items)
    return {"record": selected}

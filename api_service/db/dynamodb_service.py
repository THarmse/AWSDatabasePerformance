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

PARAM_NAME = "/Liverpool/DynamoDB/Credentials"

# --------- Global session/resource/table reuse ---------
_creds = json.loads(get_db_credentials(PARAM_NAME))
_session = boto3.Session(region_name=_creds["region"])
_dynamodb_resource = _session.resource(
    "dynamodb",
    endpoint_url=_creds.get("endpoint")
)
_table = _dynamodb_resource.Table(_creds["table_name"])
# ------------------------------------------------------------

async def get_table():
    """
    Returns the globally initialized boto3 Table resource.
    """
    return _table

async def initialize_table():
    """
    Checks if the table exists. If not, creates it.
    """
    table_name = _creds["table_name"]

    try:
        _table.load()
        return {"message": f"Table '{table_name}' already exists in DynamoDB."}
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceNotFoundException':
            return {"error": str(e)}
        # Create the table
        new_table = _dynamodb_resource.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'transaction_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'transaction_id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        new_table.wait_until_exists()
        return {"message": f"Table '{table_name}' created successfully in DynamoDB."}

async def load_sample_data():
    """
    Inserts 1 random sample record into the transaction_records table.
    """
    await insert_transaction(record=None)
    return {"message": "1 sample record inserted successfully into DynamoDB."}

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

    record["transaction_id"] = str(uuid.uuid4())

    try:
        table = await get_table()
        table.put_item(Item=record)
        return {"message": "Record inserted successfully into DynamoDB.", "transaction_id": record["transaction_id"]}
    except ClientError as e:
        return {"error": str(e)}

async def select_transaction():
    """
    Retrieves one random transaction record from the DynamoDB table.
    """
    try:
        table = await get_table()
        scan_response = table.scan(Limit=1)
        items = scan_response.get("Items", [])
        if not items:
            return {"message": "No records found in the DynamoDB table."}
        selected = random.choice(items)
        return {"record": selected}
    except ClientError as e:
        return {"error": str(e)}

async def update_random_transaction_status():
    """
    Updates the 'status' field of one random transaction record in DynamoDB.
    Selects a new random status from predefined options.
    """
    statuses = ["Completed", "Pending", "Failed", "Refunded"]
    new_status = random.choice(statuses)

    try:
        table = await get_table()
        scan_response = table.scan(Limit=1)
        items = scan_response.get("Items", [])
        if not items:
            return {"message": "No records found to update in the DynamoDB table."}

        selected = random.choice(items)
        transaction_id = selected["transaction_id"]

        table.update_item(
            Key={"transaction_id": transaction_id},
            UpdateExpression="SET #s = :status",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":status": new_status}
        )
        return {"message": f"Updated status to '{new_status}' for transaction_id {transaction_id} in DynamoDB."}
    except ClientError as e:
        return {"error": str(e)}

async def delete_random_transaction():
    """
    Deletes one random transaction record from the DynamoDB table.
    """
    try:
        table = await get_table()
        scan_response = table.scan(Limit=1)
        items = scan_response.get("Items", [])
        if not items:
            return {"message": "No records found to delete in the DynamoDB table."}

        selected = random.choice(items)
        transaction_id = selected["transaction_id"]

        table.delete_item(Key={"transaction_id": transaction_id})
        return {"message": f"Deleted transaction with ID {transaction_id} from DynamoDB."}
    except ClientError as e:
        return {"error": str(e)}

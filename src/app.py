import json
import os
from decimal import Decimal

import boto3


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def decimal_to_native(obj):
    if isinstance(obj, list):
        return [decimal_to_native(i) for i in obj]

    if isinstance(obj, dict):
        return {k: decimal_to_native(v) for k, v in obj.items()}

    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)

    return obj


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    method = event.get("httpMethod")
    path_params = event.get("pathParameters") or {}

    # GET /items → list all items
    if method == "GET" and "id" not in path_params:
        result = table.scan()
        items = decimal_to_native(result.get("Items", []))
        return response(200, items)

    # GET /items/{id} → fetch single item
    if method == "GET" and "id" in path_params:
        item_id = path_params["id"]
        result = table.get_item(Key={"id": item_id})
        item = result.get("Item")

        if not item:
            return response(404, {"message": "Item not found"})

        return response(200, decimal_to_native(item))

    # POST /items → create item
    if method == "POST":
        if not event.get("body"):
            return response(400, {"message": "Request body is required"})

        body = json.loads(event["body"])

        if "id" not in body:
            return response(400, {"message": "Field 'id' is required"})

        table.put_item(Item=body)
        return response(201, body)

    return response(405, {"message": "Method Not Allowed"})

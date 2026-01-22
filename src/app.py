import json
import boto3
import os
from decimal import Decimal


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
    method = event["httpMethod"]
    path_params = event.get("pathParameters") or {}

    # GET /items → list all
    if method == "GET" and "id" not in path_params:
        re

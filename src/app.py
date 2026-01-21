import json
import os
import uuid

import boto3


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    method = event["httpMethod"]

    if method == "POST":
        item = json.loads(event["body"])
        item["id"] = str(uuid.uuid4())
        table.put_item(Item=item)
        return response(201, item)

    if method == "GET":
        item_id = event["pathParameters"]["id"]
        result = table.get_item(Key={"id": item_id})
        return response(200, result.get("Item"))

    if method == "PUT":
        item_id = event["pathParameters"]["id"]
        data = json.loads(event["body"])
        data["id"] = item_id
        table.put_item(Item=data)
        return response(200, data)

    if method == "DELETE":
        item_id = event["pathParameters"]["id"]
        table.delete_item(Key={"id": item_id})
        return response(204, None)


def response(status, body):
    return {
        "statusCode": status,
        "body": json.dumps(body) if body else "",
    }

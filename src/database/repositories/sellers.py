from typing import Dict, List

from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

from database.dynamodb import dynamodb

table = dynamodb.Table("sellers")


def get_seller_by_id(telegram_user_id: int):
    try:
        response = table.get_item(Key={"telegram_user_id": telegram_user_id})
    except ClientError as e:
        print(f"❌ Fehler beim Zugriff auf DynamoDB: {e.response['Error']['Message']}")
        return None

    return response.get("Item")


def save_seller(seller_data: dict):
    table.put_item(Item=seller_data)


def update_seller_field(telegram_user_id: int, field: str, value: any):
    table.update_item(
        Key={"telegram_user_id": telegram_user_id},
        UpdateExpression=f"SET {field} = :val",
        ExpressionAttributeValues={":val": value},
    )


def delete_seller_by_id(telegram_user_id: int):
    try:
        telegram_user_id = int(telegram_user_id)
        key = {"telegram_user_id": telegram_user_id}
        response = table.get_item(Key=key)
        item = response.get("Item")
        if not item:
            raise ValueError("Verkäufer nicht gefunden.")

        table.delete_item(Key=key)
        return True
    except ClientError as e:
        print(f"❌ Fehler beim Zugriff auf DynamoDB: {e.response['Error']['Message']}")
        raise
    except Exception as e:
        print(f"❌ Allgemeiner Fehler: {e}")
        raise


def set_seller_as_registered(telegram_user_id: int):
    try:
        telegram_user_id = int(telegram_user_id)
        key = {"telegram_user_id": telegram_user_id}
        response = table.get_item(Key=key)
        item = response.get("Item")
        if not item:
            raise ValueError("Verkäufer nicht gefunden.")

        table.update_item(
            Key=key,
            UpdateExpression="SET registered = :r",
            ExpressionAttributeValues={":r": True},
        )
        return True
    except ClientError as e:
        print(f"❌ Fehler beim Zugriff auf DynamoDB: {e.response['Error']['Message']}")
        raise
    except Exception as e:
        print(f"❌ Allgemeiner Fehler: {e}")
        raise


def get_all_sellers() -> List[Dict]:
    try:
        response = table.scan()
        return response.get("Items", [])
    except Exception as e:
        print(f"[ERROR] Fehler beim Abrufen der Verkäufer: {e}")
        return []


# Zählt alle Items
def count_all_items() -> int:
    count = 0
    response = table.scan(ProjectionExpression="seller_status")
    count += len(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"],
            ProjectionExpression="seller_status",
        )
        count += len(response.get("Items", []))
    return count


# Zählt gefilterte Items
def count_items_filtered(filter_expr) -> int:
    count = 0
    response = table.scan(
        FilterExpression=filter_expr,
        ProjectionExpression="seller_status",  # Optional: reduziert Rückgabedaten
    )
    count += len(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"],
            FilterExpression=filter_expr,
            ProjectionExpression="seller_status",
        )
        count += len(response.get("Items", []))
    return count

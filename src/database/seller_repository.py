from botocore.exceptions import ClientError

from database.dynamodb import dynamodb

table = dynamodb.Table("seller")


def get_seller_by_id(telegram_user_id: int):
    try:
        response = table.get_item(Key={"telegram_user_id": telegram_user_id})
    except ClientError as e:
        print(f"❌ Fehler beim Zugriff auf DynamoDB: {e.response['Error']['Message']}")
        return None

    return response.get("Item")


def save_seller(seller_data: dict):
    table.put_item(Item=seller_data)


def delete_seller_by_id(telegram_user_id: int):
    try:
        item = table.get_item(Key={"telegram_user_id": telegram_user_id})
    except ClientError as e:
        print(f"❌ Fehler beim Zugriff auf DynamoDB: {e.response['Error']['Message']}")

    return table.delete_item(item)

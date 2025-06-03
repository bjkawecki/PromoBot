from datetime import datetime
from decimal import Decimal

from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

from database.dynamodb import dynamodb

table = dynamodb.Table("promotions")


def safe_parse_decimal(value, default=Decimal("0.0")) -> Decimal:
    if value is None:
        return default
    try:
        cleaned = str(value).strip().replace(",", ".").replace("€", "")
        return Decimal(cleaned)
    except Exception:
        raise ValueError(f"Ungültiger numerischer Wert: {value}")


def create_promotion(data: dict):
    item = {
        "promo_id": data.get("promo_id"),  # Sort Key
        "seller_id": data.get("seller_id"),  # Sort Key
        "start_date": data.get("start_date"),  # ISO-Format erwartet: '2025-05-26'
        "end_date": data.get("end_date"),
        "display_name": data.get("display_name"),
        "image": data.get("image"),
        "description": data.get("description"),
        "price": safe_parse_decimal(data.get("price", 0.0)),
        "shipping_costs": safe_parse_decimal(data.get("shipping_costs", 0.0)),
        "display_message": data.get("display_message"),
        "channel_id": data.get("channel_id"),
        "created_at": datetime.utcnow().isoformat() + "Z",
    }

    try:
        table.put_item(Item=item)
        success_msg = "✅ Angebot erfolgreich gespeichert."
        print(success_msg)
        return True, success_msg
    except Exception as e:
        error_msg = f"❌ Fehler beim Speichern: {e}"
        print(error_msg)
        return False, error_msg


def get_promotions_by_seller_id(seller_id: int):
    try:
        response = table.query(
            KeyConditionExpression=Key("seller_id").eq(seller_id),
            FilterExpression=Attr("promo_status").ne("deleted"),
        )
        return response.get("Items", [])
    except Exception as e:
        print(f"❌ Fehler beim Abfragen der Promos: {e}")
        return []


def get_promotion_list():
    try:
        response = table.scan()
        items = response.get("Items", [])

        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            items.extend(response.get("Items", []))

        return items

    except Exception as e:
        print(f"❌ Fehler beim Abfragen der Promos: {e}")
        return []


def count_promos_for_seller(seller_id_raw: int) -> int:
    seller_id = int(seller_id_raw)
    table = dynamodb.Table("promotions")
    response = table.query(
        KeyConditionExpression=Key("seller_id").eq(seller_id),
        FilterExpression=Attr("promo_status").ne("deleted"),
    )
    return len(response.get("Items", []))


def count_active_promos_for_seller(seller_id: int) -> int:
    from datetime import date

    today = date.today().isoformat()
    table = dynamodb.Table("promotions")
    response = table.query(
        KeyConditionExpression=Key("seller_id").eq(seller_id),
        FilterExpression=Attr("start_date").lte(today)
        & Attr("end_date").gte(today)
        & Attr("promo_status").ne("deleted"),
    )
    return len(response.get("Items", []))


def get_promo_by_promo_id_and_seller_id(promo_id: str, seller_id: int):
    try:
        response = table.get_item(Key={"promo_id": promo_id, "seller_id": seller_id})
    except ClientError as e:
        print(f"❌ Fehler beim Zugriff auf DynamoDB: {e.response['Error']['Message']}")
        return None
    return response.get("Item")


def get_promo_by_promo_id(promo_id: str):
    try:
        response = table.scan(FilterExpression=Attr("promo_id").eq(promo_id))
        items = response.get("Items", [])
        return items[0] if items else None
    except ClientError as e:
        print(f"❌ Fehler beim Zugriff auf DynamoDB: {e.response['Error']['Message']}")
        return None


def save_promo(promo_data: dict):
    table.put_item(Item=promo_data)


def get_promo_field(promo_id: str, seller_id: int, field) -> str | None:
    try:
        response = table.get_item(Key={"promo_id": promo_id, "seller_id": seller_id})
    except ClientError as e:
        print(f"❌ Fehler beim Zugriff auf DynamoDB: {e.response['Error']['Message']}")
        return None

    item = response.get("Item")
    if not item:
        return None

    return item.get(field)


def update_promo_field(promo_id: int, seller_id: str, field: str, new_value: any):
    table.update_item(
        Key={"promo_id": promo_id, "seller_id": seller_id},
        UpdateExpression=f"SET {field} = :val",
        ExpressionAttributeValues={":val": new_value},
    )


def set_promo_status_to_deleted(promo_id: int, seller_id: str):
    try:
        table.update_item(
            Key={"promo_id": promo_id, "seller_id": seller_id},
            UpdateExpression="SET promo_status = :deleted",
            ExpressionAttributeValues={":deleted": "deleted"},
        )
    except Exception as e:
        print(f"❌ Fehler beim Löschen: {e}")

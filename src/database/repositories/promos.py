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
        "promo_id": data.get("promo_id"),
        "seller_id": data.get("seller_id"),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "display_name": data.get("display_name"),
        "image": data.get("image"),
        "description": data.get("description"),
        "price": safe_parse_decimal(data.get("price", 0.0)),
        "shipping_costs": safe_parse_decimal(data.get("shipping_costs", 0.0)),
        "display_message": data.get("display_message"),
        "channel_id": data.get("channel_id"),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "promo_status": "inactive",
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


# Zählt alle Items
def count_all_promos() -> int:
    count = 0
    response = table.scan(ProjectionExpression="promo_status")
    count += len(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"],
            ProjectionExpression="promo_status",
        )
        count += len(response.get("Items", []))
    return count


# Zählt gefilterte Items
def count_promos_filtered(filter_expr) -> int:
    count = 0
    response = table.scan(
        FilterExpression=filter_expr,
        ProjectionExpression="promo_status",  # Optional: reduziert Rückgabedaten
    )
    count += len(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"],
            FilterExpression=filter_expr,
            ProjectionExpression="promo_status",
        )
        count += len(response.get("Items", []))
    return count


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
        response = table.update_item(
            Key={"promo_id": promo_id, "seller_id": seller_id},
            UpdateExpression="SET promo_status = :deleted",
            ExpressionAttributeValues={":deleted": "deleted"},
            ReturnValues="UPDATED_NEW",
        )
        soft_deleted_item = response.get("Attributes")
        if soft_deleted_item.get("promo_status") == "deleted":
            print(f"✅ Promo als gelöscht markiert: {promo_id} (Seller: {seller_id})")
        else:
            print("⚠️ Kein Item zurückgegeben (möglicherweise war es leer).")
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print(
                f"❌ Promo nicht gefunden oder bereits gelöscht: {promo_id} (Seller: {seller_id})"
            )
        else:
            print(
                f"❌ Fehler beim Löschen der Promo {promo_id} (Seller: {seller_id}): {e.response['Error']['Message']}"
            )
        return False


def hard_delete_promo(promo_id: str, seller_id: int) -> bool:
    try:
        response = table.delete_item(
            Key={"promo_id": promo_id, "seller_id": seller_id},
            ConditionExpression="attribute_exists(promo_id)",
            ReturnValues="ALL_OLD",  # Gibt das gelöschte Item zurück (falls vorhanden)
        )
        deleted_item = response.get("Attributes")
        if deleted_item:
            print(f"✅ Promo gelöscht: {promo_id} (Seller: {seller_id})")
        else:
            print("⚠️ Kein altes Item zurückgegeben (möglicherweise war es leer).")
        return True

    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print(
                f"❌ Promo nicht gefunden oder bereits gelöscht: {promo_id} (Seller: {seller_id})"
            )
        else:
            print(
                f"❌ Fehler beim Löschen der Promo {promo_id} (Seller: {seller_id}): {e.response['Error']['Message']}"
            )
        return False

import uuid
from datetime import datetime

from boto3.dynamodb.conditions import Key

from database.dynamodb import dynamodb

table = dynamodb.Table("promotions")


def create_promotion(data: dict):
    item = {
        "promotion_id": data.get("promo_id"),  # Sort Key
        "start_date": data.get("start_date"),  # ISO-Format erwartet: '2025-05-26'
        "end_date": data.get("end_date"),
        "display_name": data.get("display_name"),
        "image_url": data.get("image_url"),
        "description": data.get("description"),
        "price": float(data.get("price", 0.0)),
        "shipping_costs": float(data.get("shipping_costs", 0.0)),
        "display_message": data.get("display_message"),
        "channel_id": int(data.get("channel_id", 0)),
        "product_limit": int(data.get("product_limit", 0)),
        "options": data.get("options", {}),
        "timer": data.get("timer", {}),
        "created_at": datetime.utcnow().isoformat() + "Z",
    }

    try:
        table.put_item(Item=item)
        print("✅ Angebot erfolgreich gespeichert.")
        return item["promotion_id"]
    except Exception as e:
        print(f"❌ Fehler beim Speichern: {e}")
        return None


def get_promotions_by_seller_id(seller_id: int):
    try:
        response = table.query(KeyConditionExpression=Key("seller_id").eq(seller_id))
        return response.get("Items", [])
    except Exception as e:
        print(f"❌ Fehler beim Abfragen der Promos: {e}")
        return []

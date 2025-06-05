NO_PROMOS_ANSWER = "❌ Verkäufer hat noch keine Promos erstellt."


def promo_image_error_message(caption: dict) -> str:
    return f"⚠️ Bild konnte nicht geladen werden, zeige nur Text:\n\n{caption}"

ORDER_ADRESS_MESSAGE = (
    "▶️ *Bestellvorgang gestartet\\.*\n\n"
    "Wir benötigen eine Versandadresse\\.\n\n"
    "*Bitte Name eingeben:*\n\n",
)

ORDER_ABORTED = "🚫 Bestellung abgebrochen."

CHANGE_ORDER_FIELD = "<b>📝 Änderung deiner Eingaben.</b>\n\nWas möchtest du ändern?"
CHANGE_NAME = "Name ändern:"
CHANGE_STREET_ADRESS = "Straße und Hausnummer ändern:"
CHANGE_CITY = "PLZ und Ort ändern:"
CHANGE_QUANTITY = "Anzahl des Produkts ändern:"


def order_summary_message(data: dict):
    name = data.get("name", "<i>Name nicht angegeben</i>")
    street_address = data.get(
        "street_address", "<i>Straße/Hausnummer nicht angegeben</i>"
    )
    city = data.get("city", "<i>PLZ/Ort nicht angegeben</i>")
    quantity = data.get("quantity", "1")
    return (
        f"<b>📦 Bestellübersicht</b>\n\n"
        f"{quantity} x Wald\\-T\\-Shirt\n\n"
        f"<b>📫 Anschrift des Empfängers:</b>\n\n"
        f"{name}\n"
        f"{street_address}\n"
        f"{city}\n\n"
        f"<b>Fahre fort, wenn alle Angaben korrekt sind.</b>"
    )

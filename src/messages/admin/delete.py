def confirm_delete_promo_message(display_name: str) -> str:
    return f"❗️Bist du sicher, dass du die Promo <b>'{display_name}'</b> aus der Datenbank löschen willst?"


def promo_deleted_message(display_name: str) -> str:
    return f"✅ Promo '{display_name}' wurde gelöscht."


def delete_error_message(e: str) -> str:
    return f"❌ Fehler beim Löschen: {e}"


def confirm_delete_seller_message(seller_info: dict) -> str:
    return (
        f"❗️<b>Bist du sicher, dass du den folgenden Verkäufer löschen möchtest?</b>\n\n"
        f"{seller_info}"
    )


def delete_seller_not_possible_message(seller_name: str, telegram_id: int) -> str:
    return (
        f"⚠️ Verkäufer {seller_name} mit ID {telegram_id} ist noch aktiv und kann daher nicht gelöscht werden.\n"
        "Bitte deaktiviere ihn zuerst."
    )


def deleted_seller_confirm_message(telegram_id: int) -> str:
    return f"✅ Verkäufer mit ID {telegram_id} wurde gelöscht."

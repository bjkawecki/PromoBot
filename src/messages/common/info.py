PROCESS_ABORTED = "❎ Vorgang abgebrochen."
NOT_AUTHORIZED_ANSWER = "Keine Berechtigung."
ERROR_PROCESSING_REQUEST = "Fehler beim Verarbeiten der Anfrage"


def error_detele_promo(e):
    return f"❌ Fehler beim Löschen der Promo: {e}"


def confirm_soft_deleted_promo(promo_name):
    return f"✅ Promo '{promo_name}' wurde gelöscht."


def error_saving(e):
    return f"❌ Fehler beim Speichern: {e}"


NO_VALIDATION_ERROR = "❌ Für dieses Feld ist keine Validierung definiert."

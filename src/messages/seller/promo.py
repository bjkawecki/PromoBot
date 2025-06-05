CREATE_PROMO_MESSAGE = (
    "📄 Neue Promo erstellen (1/9)\n\n<b>Wie heißt deine Promo?</b>\n\n"
    "Der Name wird als <b>Überschrift</b> in der Werbenachricht angezeigt.\n\n"
    "(Beispiel: 🎄 <i>Weihnachtsangebot 2025</i>)",
)

EDIT_PROMO_MESSAGE = "<b>Promo bearbeiten</b>\n\nWähle ein Feld zum Bearbeiten:"


def confirm_promo_created_message(display_name):
    return f"<b>✅ Neue Promo '{display_name}' wurde erstellt</b>."


def edit_promo_field_message(field_label, field_value):
    return (
        f"<b>Änderung der Promo</b>\n\n"
        f"<b>{field_label}:</b> {field_value}\n\n"
        "📝 Bitte mach eine neue Eingabe."
    )


CONFIRM_UPDATED_PROMO_ANSWER = "✅ Promo wurde aktualisiert."

NO_PROMOS_ANSWER = "❌ Du hast noch keine Promos erstellt."


def confirm_toggle_promo_status(action):
    return (
        "❗️<b>Bist du sicher, dass du die Promo "
        f"{'aktivieren' if action == 'a' else 'deaktivieren'} möchtest?</b>\n\n"
    )


def confirm_toggled_promo(promo_status):
    return (
        "✅ Promo wurde aktiviert."
        if promo_status == "active"
        else "🚫 Promo wurde deaktiviert."
    )


CONFIRM_SAVE_PROMO_MESSAGE = (
    "Neue Promo erstellen: abgeschlossen\n\nEingaben speichern?"
)


def promo_validate_name_answer(max_length):
    return (
        f"❌ Der Titel muss zwischen 3 und {max_length} Zeichen lang sein.\n\n"
        "Bitte versuche es erneut oder drücke auf 'Abbrechen':"
    )


PROMO_ADD_MESSAGE = (
    "📄 Neue Promo erstellen (2/9)\n\n<b>Erstelle eine Nachricht</b>\n\n"
    "Dieser Text erscheint im Beitrag unter dem Titel.\n\n"
    "(Beispiel: <i>Bestelle Buch XY mit Gratisversand.</i>)"
)


def promo_validate_message_answer(max_length):
    return (
        f"❌ Die Nachricht muss zwischen 3 und {max_length} Zeichen lang sein.\n\n"
        "Bitte versuche es erneut oder drücke auf 'Abbrechen':"
    )


PROMO_ADD_PRICE = (
    "📄 Neue Promo erstellen (3/9)\n\n<b>Gib den Preis ohne Versandkosten an</b>\n\n"
    "Zahl mit maximal zwei Nachkommastellen, ohne Eurozeichen.\n\n"
    "(Beispiel: 12,99)"
)


PROMO_VALIDATE_PRICE_ANSWER = "Falsches Format. Bitte probiere es erneut."

PROMO_ADD_SHIPPING_COSTS = (
    "📄 Neue Promo erstellen (4/9)\n\n<b>Gib die Versandkosten an</b>\n\n"
    "Zahl mit maximal zwei Nachkommastellen, ohne Eurozeichen.\n\n"
    "(Beispiel: 3,99)"
)

PROMO_ADD_DESCRIPTION = (
    "📄 Neue Promo erstellen (5/9)\n\n<b>Erstelle eine Beschreibung</b>\n\n"
    "Ein detaillierte Beschreibung, die Käufer bei der Interaktion mit dem Bot abrufen können."
)


def promo_validate_description_answer(max_length):
    return (
        f"❌ Die Beschreibung muss zwischen 3 und {max_length} Zeichen lang sein.\n\n"
        "Bitte versuche es erneut oder drücke auf 'Abbrechen':"
    )


PROMO_ADD_CHANNEL_ID = (
    "📄 Neue Promo erstellen (6/9)\n\n<b>Gib die Kanal-Id an</b>\n\n"
    "Die Id des Ausgabekanals, in den der Bot die Promo posten soll.\n\n"
    "(Bot und Verkäufer müssen Zugriff auf diesen Kanal haben.)"
)

PROMO_ADD_START_DATE = (
    "📄 Neue Promo erstellen (7/9)\n\n<b>Gib das Startdatum ein</b>\n\n"
    "Ab diesem Datum darf die Promo im Ausgabekanal gepostet werden.\n\n"
    "Die Eingabe muss das Format DD.MM.YYYY haben. (Beispiel: 20.10.2025)"
)

PROMO_ADD_END_DATE = (
    "📄 Neue Promo erstellen (8/9)\n\n<b>Gib das Startdatum ein</b>\n\n"
    "Bis zu diesem Datum darf die Promo im Ausgabekanal gepostet werden.\n\n"
    "Die Eingabe muss das Format DD.MM.YYYY haben. (Beispiel: 01.11.2025)"
)

PROMO_ADD_IMAGE = (
    "📄 Neue Promo erstellen (9/9)\n\n<b>Füge ein Bild hinzu</b>\n\n"
    "Das Bild wird Teil der Werbenachricht."
)

PROMO_IMAGE_FORMAT_ERROR = "Bitte sende ein JPEG- oder PNG-Bild."


def confirm_edit_promo_field_message(field_label, field_value):
    return f"<b>Neue Eingabe für {field_label}:</b>\n\n{field_value}\n\n💾 <b>Eingabe speichern?</b>"

def register_add_company_name_message(company_name):
    return (
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {company_name}\n"
        "\nBitte gib den <b>Anzeigename</b> deines Unternehmens an:"
    )


def register_add_contact_name_message(data: dict, display_name):
    return (
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('company_name')}\n"
        f"Anzeigename: {display_name}\n"
        "\nBitte gib einen <b>Ansprechpartner</b> an:"
    )


def register_add_email_message(data: dict, contact_name):
    return (
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('company_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"Ansprechpartner: {contact_name}\n"
        "\nBitte gib eine <b>geschäftliche E-Mail-Adresse</b> an:"
    )


def register_add_website_message(data: dict, contact_phone):
    return (
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('company_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email')}\n"
        f"Telefon: {contact_phone}\n"
        "\nBitte gib die <b>Webseite</b> deiner Firma an (optional):"
    )


def register_add_stripe_account_id(data: dict):
    return (
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('company_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email', '–')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        f"Webseite: {data.get('website', '–')}\n"
        "\nBitte gib die <b>ID deines Stripe-Kontos</b> an (optional, benötigt für das Starten von Promos):"
    )


def register_add_phone_message(data, contact_email):
    return (
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('company_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {contact_email}\n"
        "\nBitte gib eine <b>geschäftliche Telefonnummer</b> an (optional):"
    )


def registration_completed_message(data):
    return (
        "📝 Registrierung als Verkäufer\n\n"
        f"Firma: {data.get('company_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email', '–')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        f"Webseite: {data.get('website', '–')}\n"
        f"Stripe-Konto-ID: {data.get('stripe_account_id', '–')}\n"
        "\n✅ <b>Der Registriervorgang als Verkäufer ist abgeschlossen!<b>\n\n"
        "Du kannst nun <b>Promos</b> hinzufügen oder dein <b>Profil</b> bearbeiten.\n\n"
    )


def confirm_edit_field_message(field_label, validated_value):
    return f"✅ Neuer Wert für <b>{field_label}</b>:\n\n{validated_value}\n\n<b>Bestätigen?</b>"

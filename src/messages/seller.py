HELP_TOPICS_INFO = (
    "<b>❓ Wie funktioniert PromoBot?</b>\n\n"
    "Mit <i>PromoBot</i> kannst du ganz einfach digitale Produkte verkaufen, direkt über Telegram.\n"
    "Erstelle dein Verkäuferprofil, verknüpfe dein Stripe-Konto, lade deine Produkte hoch und verkaufe sofort.\n"
    "Keine Website nötig, alles läuft im Chat.\n\n"
    "❓ <b>Wie werde ich über neue Käufe benachrichtigt?</b>\n\n"
    "Du bekommst sofort eine Nachricht im Bot, wenn jemand dein Produkt kauft.\n"
    "Je nach Produktart kannst du automatische Downloads oder Nachrichten versenden lassen.\n"
    "Optional kannst du E-Mail-Benachrichtigungen aktivieren."
)

HELP_TOPICS_STRIPE = (
    "<b>❓ Wie verknüpfe ich mein Stripe-Konto</b>\n\n"
    "1. Registriere dich auf https://stripe.com/de.\n"
    "2. Gib deine Stripe-Konto-ID in deinem PromoBot-Käuferprofil an.\n\n"
    "<b>❓ Wann erhalte ich meine Auszahlungen?</b>\n\n"
    "Die Auszahlung erfolgt über Stripe.\n"
    "Du kannst in deinem Stripe-Dashboard einstellen, ob du tägliche, wöchentliche oder monatliche Auszahlungen erhalten möchtest.\n"
    "Standardmäßig zahlt Stripe nach etwa 7 Tagen ab dem Kaufdatum aus.\n\n"
    "❓ <b>Was tun bei Stornierungen?</b>\n\n"
    "Käufer können nur in Ausnahmefällen eine Rückerstattung beantragen.\n"
    "Falls eine Stornierung notwendig ist:\n\n"
    "- Du wirst benachrichtigt.\n"
    "- Die Rückzahlung erfolgt über Stripe.\n"
    "- Gebühren können anfallen (abhängig von Stripe).\n\n"
    "Wende dich bei Fragen an den Support."
)

HELP_TOPICS_SUPPORT = (
    "❓ <b>Kontakt zum Support-Team</b>\n\n"
    "Brauchst du Hilfe? Schreib uns direkt hier im Chat:\n"
    "👉 Support kontaktieren\n"
    "Oder per E-Mail:\n"
    "📧 support@deineplattform.de\n"
    "Wir antworten in der Regel innerhalb von 24 Stunden."
)
HELP_TOPICS_LEGAL = (
    "❓ <b>Nutzungsbedingungen & Datenschutz</b>\n\n"
    "Mit dem Verkauf über unsere Plattform stimmst du den Nutzungsbedingungen zu.\n"
    "Wir behandeln deine Daten gemäß unserer Datenschutzerklärung.\n"
    "Du bist für deine Produkte und Inhalte selbst verantwortlich."
)


HELP_TOPICS = {
    "info": HELP_TOPICS_INFO,
    "stripe": HELP_TOPICS_STRIPE,
    "support": HELP_TOPICS_SUPPORT,
    "legal": HELP_TOPICS_LEGAL,
}

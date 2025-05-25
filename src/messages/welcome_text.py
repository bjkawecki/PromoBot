welcome_text = (
    "*👋 Willkommen bei PromoBot\!*\n\n"
    "🌟 *Exklusiver Rabatt für Kanal\-Abonnenten*\:\n\n"
    "*🌲 Wald\-T\-Shirt – stylisch, nachhaltig, bequem*\n\n"
    "*Verfügbare Größen:* XS, S, M, L, XL\n"
    "*Farben:* Blau, Rot, Gelb\n\n"
    "*💸 Statt ~30~€ nur 20€\!* 🔥\n"
    "_Nur für kurze Zeit verfügbar_\n\n"
    "📅 *Gültig bis:* *30\. Juni*"
)


def get_role_welcome_message_text(role: str):
    if role == "admin":
        return "Willkommen, Admin!"
    elif role == "seller":
        return "Hallo Verkäufer!"
    else:
        return "Willkommen, Kunde!"

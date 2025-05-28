welcome_text = (
    "*Willkommen bei PromoBot!*\n\n"
    "🌟 *Exklusiver Rabatt für Kanal\\-Abonnenten*:\n\n"
    "*Wald\\-T\\-Shirt – stylisch, nachhaltig, bequem*\n\n"
    "*Verfügbare Größen:* XS, S, M, L, XL\n"
    "*Farben:* Blau, Rot, Gelb\n\n"
    "*💸 Statt ~30~€ nur 20€!* 🔥\n"
    "_Nur für kurze Zeit verfügbar_\n\n"
    "📅 *Gültig bis:* *30\\. Juni*"
)


def get_role_welcome_message_text(role: str, seller):
    if role == "admin":
        return "Willkommen, Admin\\!"
    elif role == "seller":
        if seller.get("active") and not seller.get("is_registered", False):
            return (
                "✉️ Du wurdest als *Verkäufer* freigeschaltet\\.\n\n"
                "*Registriere* dich, um Promos zu erstellen\\."
            )
        elif not seller.get("active") and seller.get("is_registered", False):
            return (
                f"Hallo, *{seller.get('display_name')}*\\.\n\n"
                "🚫 Dein Konto bei PromoBot ist *nicht aktiv*\\.\n\n"
                "💬 Kontaktiere den *Administrator*, um dein Konto zu aktivieren\\."
            )
        else:
            registered_seller_text = f"Hallo, *{seller.get('display_name')}*\\.\n\n✅ Dein Konto bei PromoBot ist *aktiv*\\."
            if not seller.get("stripe_account_id", False):
                registered_seller_text += "\n\n⚠️ Du hast *keine Stripe\\-ID* hinterlegt\\. Du benötigst eine Stripe\\-ID, um *Promos* zu starten\\."
            else:
                registered_seller_text += "\n\n💬 Erstelle und verwalte *Promos*\\.\n\nErstellte Promos: 0\nAktive Promos: 0"
            return registered_seller_text
    else:
        return "Willkommen, Kunde\\!"

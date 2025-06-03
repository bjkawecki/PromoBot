from database.repositories.promos import count_promos_for_seller

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
        return "*Willkommen, Admin*\\!\n\n🗂 Verwalte Verkäufer und ihre Promos\\.\n\nAktuell gibt es"
    elif role == "seller":
        seller_status = seller.get("seller_status")
        if seller_status == "active" and not seller.get("is_registered", False):
            return (
                "✉️ Du wurdest als *Verkäufer* freigeschaltet\\.\n\n"
                "*Registriere* dich, um Promos zu erstellen\\."
            )
        elif seller_status == "inactive" and seller.get("is_registered", False):
            return (
                f"Hallo, *{seller.get('display_name')}*\\.\n\n"
                "🚫 Dein Konto bei PromoBot ist *deaktiviert*\\.\n\n"
                "💬 Wenn du denkst, dass dein Konto aktiv sein sollte, kontaktiere den *Support*\\."
            )
        else:
            created_promos = count_promos_for_seller(seller.get("telegram_user_id"))
            registered_seller_text = f"Hallo, *{seller.get('display_name')}*\\.\n\n✅ Dein Konto bei PromoBot ist *aktiv*\\."
            if not seller.get("stripe_account_id", False):
                registered_seller_text += "\n\n⚠️ Du hast *keine Stripe\\-ID* hinterlegt\\. Du benötigst eine Stripe\\-ID, um *Promos* zu starten\\."
            else:
                registered_seller_text += (
                    f"\n\n💬 Erstelle und verwalte *Promos*\\.\n\n"
                    f"Erstellte Promos: {created_promos}\n"
                    f"Aktive Promos: 0"
                )
            return registered_seller_text
    else:
        return "Willkommen, Kunde\\!"

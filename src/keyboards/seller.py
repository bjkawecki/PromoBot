from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_registered_seller_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Promo erstellen", callback_data="seller_products"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📁 Promos verwalten", callback_data="seller_products"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👤 Profil bearbeiten", callback_data="update_seller_profile"
                )
            ],
            [InlineKeyboardButton(text="❓ Hilfe", callback_data="seller_help_menu")],
            [InlineKeyboardButton(text="↩️ Neustart", callback_data="back_to_start")],
        ]
    )


def get_unregistered_seller_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📜 Registrieren", callback_data="register_seller"
                )
            ],
            [InlineKeyboardButton(text="❓ Hilfe", callback_data="seller_help_menu")],
            [InlineKeyboardButton(text="↩️ Neustart", callback_data="back_to_start")],
        ]
    )


def get_optional_phone_field_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Überspringen", callback_data="skip_add_phone"
                ),
            ],
            [
                InlineKeyboardButton(text="Abbrechen", callback_data="back_to_start"),
            ],
        ]
    )


def get_optional_website_field_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Überspringen", callback_data="skip_add_website"
                ),
            ],
            [
                InlineKeyboardButton(text="Abbrechen", callback_data="back_to_start"),
            ],
        ]
    )


def get_optional_stripe_id_field_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Überspringen", callback_data="skip_add_stripe_id"
                ),
            ],
            [
                InlineKeyboardButton(text="Abbrechen", callback_data="back_to_start"),
            ],
        ]
    )


def get_update_seller_profile_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Unternehmensname",
                    callback_data="edit_seller_profile_field:company_name",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Anzeigename",
                    callback_data="edit_seller_profile_field:display_name",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Ansprechpartner",
                    callback_data="edit_seller_profile_field:contact_name",
                )
            ],
            [
                InlineKeyboardButton(
                    text="E-Mail", callback_data="edit_seller_profile_field:email"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Webseite", callback_data="edit_seller_profile_field:website"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Telefon", callback_data="edit_seller_profile_field:phone"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Stripe-Konto-ID",
                    callback_data="edit_seller_profile_field:stripe_account_id",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Zum Hauptmenü", callback_data="back_to_start"
                )
            ],
        ]
    )


def get_abort_update_seller_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Abbrechen", callback_data="update_seller_profile"
                )
            ]
        ]
    )


def get_back_to_update_seller_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Zur Übersicht", callback_data="update_seller_profile"
                )
            ]
        ]
    )


def get__update_seller_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Abbrechen", callback_data="update_seller_profile"
                )
            ]
        ]
    )


def get_confirm_update_seller_field_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Bestätigen",
                    callback_data="confirm_seller_profile_update_field",
                ),
                InlineKeyboardButton(
                    text="❌ Abbrechen", callback_data="update_seller_profile"
                ),
            ]
        ]
    )


def get_seller_help_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Allgemeine Informationen", callback_data="seller_help:info"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Bezahlen mit Stripe", callback_data="seller_help:stripe"
                )
            ],
            [InlineKeyboardButton(text="Support", callback_data="seller_help:support")],
            [
                InlineKeyboardButton(
                    text="AGB & Datenschutz", callback_data="seller_help:legal"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Zum Hauptmenü", callback_data="back_to_start"
                )
            ],
        ]
    )


def get_back_to_seller_help_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Zurück", callback_data="seller_help_menu")]
        ]
    )

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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


def get_update_seller_keyboard() -> InlineKeyboardMarkup:
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

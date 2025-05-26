from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_registered_seller_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Produkte verwalten", callback_data="seller_products"
                )
            ],
            [InlineKeyboardButton(text="↩️ Neustart", callback_data="back_to_start")],
        ]
    )


def get_unregistered_seller_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Jetzt registrieren", callback_data="register_seller"
                )
            ],
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


def get_optional_homepage_field_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Überspringen", callback_data="skip_add_homepage"
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

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
                    text="Registrieren", callback_data="seller_register"
                )
            ],
            [InlineKeyboardButton(text="↩️ Neustart", callback_data="back_to_start")],
        ]
    )

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def seller_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Produkte verwalten", callback_data="seller_products"
                )
            ]
        ]
    )

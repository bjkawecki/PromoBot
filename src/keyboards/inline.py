from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Produkt ansehen", callback_data="show_product"
                ),
                InlineKeyboardButton(text="Jetzt bestellen", callback_data="order_now"),
            ],
            [
                InlineKeyboardButton(
                    text="Meine Bestellungen", callback_data="my_orders"
                ),
                InlineKeyboardButton(
                    text="Hilfe / Support", callback_data="help_support"
                ),
            ],
        ]
    )
    return keyboard

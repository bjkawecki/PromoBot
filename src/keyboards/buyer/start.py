from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_buyer_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Meine Bestellungen", callback_data="buyer_orders"
                )
            ]
        ]
    )


def get_main_menu_deeplink() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Bestellung starten", callback_data="collect_order_details"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Produktbeschreibung",
                    callback_data="product_details_menu",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❓ Hilfe", callback_data="display_bot_help_options"
                ),
            ],
        ]
    )
    return keyboard

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_neutral() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📦 Meine Bestellungen", callback_data="my_orders"
                ),
            ],
            [
                InlineKeyboardButton(text="🛍️ Meine Käufe", callback_data="my_orders"),
            ],
            [
                InlineKeyboardButton(
                    text="Alle aktuellen Aktionen ansehen", callback_data="all_promos"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❓ Hilfe / Support", callback_data="help_support"
                ),
            ],
        ]
    )
    return keyboard


def get_main_menu_deeplink() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Bestellung starten", callback_data="enter_order_info"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Produktdetails", callback_data="get_product_description"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❓ Hilfe", callback_data="get_order_support"
                ),
            ],
        ]
    )
    return keyboard

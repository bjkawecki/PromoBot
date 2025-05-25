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
                    text="❓ Hilfe / Support", callback_data="display_bot_help_options"
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
                    text="✅ Bestellung starten", callback_data="collect_order_details"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Produktbeschreibung",
                    callback_data="display_product_description",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❓ Hilfe", callback_data="display_bot_help_options"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Sende Werbenachricht", callback_data="send_product_promo"
                )
            ],
        ]
    )
    return keyboard

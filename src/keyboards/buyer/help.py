from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_help_options_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📦 Bestellung und Bezahlung", callback_data="how_to_order"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🚚 Abruf des Lieferstatus",
                    callback_data="how_to_get_order_status",
                ),
            ],
            [InlineKeyboardButton(text="🔐 Datenschutz", callback_data="data_privacy")],
            [
                InlineKeyboardButton(
                    text="🔙 Hauptmenü", callback_data="back_to_start"
                ),
            ],
        ]
    )
    return keyboard


def get_back_to_help_options_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Zurück zum Hilfemenu",
                    callback_data="display_bot_help_options",
                ),
            ],
        ]
    )
    return keyboard

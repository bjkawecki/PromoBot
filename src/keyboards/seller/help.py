from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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
            [InlineKeyboardButton(text="⬅️ Hauptmenu", callback_data="seller_help_menu")]
        ]
    )

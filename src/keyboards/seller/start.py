from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_registered_seller_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Bestellungen", callback_data="list_orders")],
            [InlineKeyboardButton(text="📢 Promos", callback_data="promo_menu")],
            [
                InlineKeyboardButton(
                    text="👤 Profil", callback_data="update_seller_profile"
                )
            ],
            [InlineKeyboardButton(text="❓ Hilfe", callback_data="seller_help_menu")],
        ]
    )


def get_unregistered_seller_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📜 Registrieren", callback_data="register_seller"
                )
            ],
            [InlineKeyboardButton(text="❓ Hilfe", callback_data="seller_help_menu")],
        ]
    )

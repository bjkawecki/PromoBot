from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_registered_seller_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Bestellungen", callback_data="list_orders")],
            [
                InlineKeyboardButton(
                    text="➕ Promo erstellen", callback_data="create_promo"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📁 Promos verwalten", callback_data="get_seller_promos"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👤 Profil bearbeiten", callback_data="update_seller_profile"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Sende Werbenachricht", callback_data="send_product_promo"
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

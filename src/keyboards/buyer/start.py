from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from messages.keyboards.confirm import (
    HELP_MENU,
    PERSONAL_ORDERS,
    PRODUCT_DESCRIPTION,
    START_ORDER,
)


def get_buyer_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=PERSONAL_ORDERS, callback_data="buyer_orders")]
        ]
    )


def get_main_menu_deeplink() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=START_ORDER, callback_data="collect_order_details"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=PRODUCT_DESCRIPTION, callback_data="product_details_menu"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=HELP_MENU, callback_data="display_bot_help_options"
                ),
            ],
        ]
    )
    return keyboard

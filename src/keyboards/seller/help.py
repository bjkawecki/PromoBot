from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from messages.keyboards.confirm import (
    MAIN_MENU,
    SELLER_HELP_MENU_INFO,
    SELLER_HELP_MENU_PRIVACY,
    SELLER_HELP_MENU_STRIPE,
    SELLER_HELP_MENU_SUPPORT,
)


def get_seller_help_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=SELLER_HELP_MENU_INFO, callback_data="seller_help:info"
                )
            ],
            [
                InlineKeyboardButton(
                    text=SELLER_HELP_MENU_STRIPE, callback_data="seller_help:stripe"
                )
            ],
            [
                InlineKeyboardButton(
                    text=SELLER_HELP_MENU_SUPPORT, callback_data="seller_help:support"
                )
            ],
            [
                InlineKeyboardButton(
                    text=SELLER_HELP_MENU_PRIVACY, callback_data="seller_help:legal"
                )
            ],
            [InlineKeyboardButton(text=MAIN_MENU, callback_data="back_to_start")],
        ]
    )


def get_back_to_seller_help_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=MAIN_MENU, callback_data="seller_help_menu")]
        ]
    )

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from messages.keyboards.confirm import (
    HELP_MENU,
    ORDER_LIST,
    PROFILE,
    PROMO_LIST,
    REGISTER_MENU,
)


def get_active_registered_seller_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ORDER_LIST, callback_data="list_orders")],
            [InlineKeyboardButton(text=PROMO_LIST, callback_data="promo_menu")],
            [InlineKeyboardButton(text=PROFILE, callback_data="update_seller_profile")],
            [InlineKeyboardButton(text=HELP_MENU, callback_data="seller_help_menu")],
        ]
    )


def get_inactive_registered_seller_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=HELP_MENU, callback_data="seller_help_menu")],
        ]
    )


def get_unregistered_seller_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=REGISTER_MENU, callback_data="register_seller")],
            [InlineKeyboardButton(text=HELP_MENU, callback_data="seller_help_menu")],
        ]
    )

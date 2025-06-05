from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from messages.keyboards.confirm import (
    HELP_DELIVERY_STATUS,
    HELP_ORDER_AND_PAYMENT,
    HELP_PRIVACY,
    MAIN_MENU,
)


def get_help_options_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=HELP_ORDER_AND_PAYMENT, callback_data="how_to_order"
                )
            ],
            [
                InlineKeyboardButton(
                    text=HELP_DELIVERY_STATUS, callback_data="how_to_get_order_status"
                )
            ],
            [InlineKeyboardButton(text=HELP_PRIVACY, callback_data="data_privacy")],
            [InlineKeyboardButton(text=MAIN_MENU, callback_data="back_to_start")],
        ]
    )
    return keyboard


def get_back_to_help_options_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=MAIN_MENU, callback_data="display_bot_help_options"
                )
            ],
        ]
    )
    return keyboard

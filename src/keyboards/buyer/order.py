from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from messages.keyboards.confirm import (
    BACK_TO_OVERVIEW,
    CANCEL,
    CITY,
    CONTINUE_TO_PAYMENT,
    EDIT_ORDER_DETAILS,
    NAME,
    QUANTITY,
    STREET_ADDRESS,
)


def get_cancel_collect_order_details_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Abbrechen", callback_data="cancel_order")]
        ]
    )
    return keyboard


def get_finish_collect_order_details_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=CONTINUE_TO_PAYMENT,
                    callback_data="continue_to_payment",
                )
            ],
            [
                InlineKeyboardButton(
                    text=EDIT_ORDER_DETAILS,
                    callback_data="edit_order_details",
                ),
            ],
            [
                InlineKeyboardButton(text=CANCEL, callback_data="cancel_order"),
            ],
        ]
    )
    return keyboard


def get_edit_order_details_back_to_summary_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BACK_TO_OVERVIEW,
                    callback_data="back_to_summary",
                )
            ],
        ]
    )
    return keyboard


def get_edit_order_details_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=NAME, callback_data="edit_name")],
            [
                InlineKeyboardButton(
                    text=STREET_ADDRESS, callback_data="edit_street_adress"
                )
            ],
            [InlineKeyboardButton(text=CITY, callback_data="edit_city")],
            [InlineKeyboardButton(text=QUANTITY, callback_data="edit_quantity")],
            [
                InlineKeyboardButton(
                    text=BACK_TO_OVERVIEW, callback_data="back_to_summary"
                )
            ],
        ]
    )
    return keyboard

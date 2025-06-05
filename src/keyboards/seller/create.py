from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from messages.keyboards.confirm import CANCEL, SKIP


def get_optional_phone_field_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=SKIP, callback_data="skip_add_phone"),
            ],
            [
                InlineKeyboardButton(text=CANCEL, callback_data="back_to_start"),
            ],
        ]
    )


def get_optional_website_field_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=SKIP, callback_data="skip_add_website"),
            ],
            [
                InlineKeyboardButton(text=CANCEL, callback_data="back_to_start"),
            ],
        ]
    )


def get_optional_stripe_id_field_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=SKIP, callback_data="skip_add_stripe_id"),
            ],
            [
                InlineKeyboardButton(text=CANCEL, callback_data="back_to_start"),
            ],
        ]
    )

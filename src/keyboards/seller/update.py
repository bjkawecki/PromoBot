from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from messages.keyboards.confirm import (
    BACK_TO_OVERVIEW,
    CANCEL,
    CONFIRM,
    EDIT_COMPANY_BUTTON,
    EDIT_CONTACT_BUTTON,
    EDIT_DISPLAY_BUTTON,
    EDIT_EMAIL_BUTTON,
    EDIT_PHONE_BUTTON,
    EDIT_STRIPE_ID_BUTTON,
    EDIT_WEBSITE_BUTTON,
    MAIN_MENU,
)


def get_update_seller_profile_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=EDIT_COMPANY_BUTTON,
                    callback_data="edit_seller_profile_field:company_name",
                )
            ],
            [
                InlineKeyboardButton(
                    text=EDIT_DISPLAY_BUTTON,
                    callback_data="edit_seller_profile_field:display_name",
                )
            ],
            [
                InlineKeyboardButton(
                    text=EDIT_CONTACT_BUTTON,
                    callback_data="edit_seller_profile_field:contact_name",
                )
            ],
            [
                InlineKeyboardButton(
                    text=EDIT_EMAIL_BUTTON,
                    callback_data="edit_seller_profile_field:contact_email",
                )
            ],
            [
                InlineKeyboardButton(
                    text=EDIT_WEBSITE_BUTTON,
                    callback_data="edit_seller_profile_field:website",
                )
            ],
            [
                InlineKeyboardButton(
                    text=EDIT_PHONE_BUTTON,
                    callback_data="edit_seller_profile_field:contact_phone",
                )
            ],
            [
                InlineKeyboardButton(
                    text=EDIT_STRIPE_ID_BUTTON,
                    callback_data="edit_seller_profile_field:stripe_account_id",
                )
            ],
            [InlineKeyboardButton(text=MAIN_MENU, callback_data="back_to_start")],
        ]
    )


def get_abort_update_seller_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=CANCEL, callback_data="update_seller_profile")]
        ]
    )


def get_back_to_update_seller_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BACK_TO_OVERVIEW, callback_data="update_seller_profile"
                )
            ]
        ]
    )


def get_update_seller_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=CANCEL, callback_data="update_seller_profile")]
        ]
    )


def get_confirm_update_seller_field_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=CONFIRM,
                    callback_data="confirm_seller_profile_update_field",
                ),
                InlineKeyboardButton(
                    text=CANCEL, callback_data="update_seller_profile"
                ),
            ]
        ]
    )

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from messages.keyboards.confirm import (
    ACTIVATE,
    ADD_SELLER,
    BACK_TO_LIST,
    CANCEL,
    CONFIRM,
    CONFIRM_DELETE,
    DEACTIVATE,
    DELETE,
    MAIN_MENU,
    PROMO_LIST,
    REPEAT_INPUT,
    SELLER_LIST,
    seller_name_or_id_button,
)


def get_abort_create_seller_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=CANCEL, callback_data="admin_sellers_menu"),
            ],
        ]
    )


def get_manage_sellers_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ADD_SELLER,
                    callback_data="add_seller",
                )
            ],
            [InlineKeyboardButton(text=SELLER_LIST, callback_data="seller_list_menu")],
            [InlineKeyboardButton(text=MAIN_MENU, callback_data="back_to_start")],
        ]
    )


def get_seller_details_menu_keyboard(
    telegram_id: int, seller_status: str
) -> InlineKeyboardMarkup:
    inline_keyboard = []

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=PROMO_LIST,
                callback_data=f"admin_seller_promo_list:{telegram_id}",
            )
        ]
    )

    if seller_status == "active":
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=DEACTIVATE,
                    callback_data=f"seller_toggle_is_active:{telegram_id}:deactivate",
                )
            ]
        )
    elif seller_status == "inactive":
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=ACTIVATE,
                    callback_data=f"seller_toggle_is_active:{telegram_id}:activate",
                )
            ]
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=DELETE,
                callback_data=f"seller_delete:{telegram_id}",
            )
        ]
    )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=BACK_TO_LIST,
                callback_data="seller_list_menu",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_confirm_toggle_keyboard(telegram_id, action):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=CONFIRM,
                    callback_data=f"confirm_toggle_seller_is_active:{telegram_id}:{action}",
                ),
                InlineKeyboardButton(
                    text=CANCEL,
                    callback_data=f"cancel_toggle_seller_is_active:{telegram_id}",
                ),
            ]
        ]
    )


def get_confirm_delete_seller_keyboard(telegram_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=CONFIRM_DELETE,
                    callback_data=f"seller_delete_confirm:{telegram_id}",
                ),
                InlineKeyboardButton(
                    text=CANCEL,
                    callback_data=f"cancel_delete_seller:{telegram_id}",
                ),
            ]
        ]
    )


def get_seller_list_keyboard(sellers: list[dict]) -> InlineKeyboardMarkup:
    buttons = []

    for seller in sellers:
        telegram_id = seller.get("telegram_user_id")
        buttons.append(
            [
                InlineKeyboardButton(
                    text=seller_name_or_id_button(seller),
                    callback_data=f"seller_details_menu:{telegram_id}",
                )
            ]
        )

    buttons.append(
        [InlineKeyboardButton(text=MAIN_MENU, callback_data="back_to_start")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_retry_or_abort_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=REPEAT_INPUT, callback_data="add_seller")],
            [InlineKeyboardButton(text=MAIN_MENU, callback_data="back_to_start")],
        ]
    )

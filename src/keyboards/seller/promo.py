from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from messages.keyboards.confirm import (
    ACTIVATE,
    BACK,
    CANCEL,
    CONFIRM,
    CONFIRM_DELETE,
    CREATE_PROMO,
    DEACTIVATE,
    DELETE_PROMO,
    EDIT_PROMO,
    MAIN_MENU,
    MANAGE_PROMOS,
    ORDER_NOW,
    PUBLISH_PROMO,
    SAVE,
)


def get_back_to_promo_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=CANCEL, callback_data="promo_menu")]
        ]
    )


def get_confirm_create_promo_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=CONFIRM, callback_data="confirm_create_promo"
                ),
                InlineKeyboardButton(text=CANCEL, callback_data="back_to_start"),
            ]
        ]
    )


def get_inline_keyboard(link) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=ORDER_NOW, url=link)]]
    )
    return keyboard


def get_promo_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=CREATE_PROMO, callback_data="create_promo")],
            [
                InlineKeyboardButton(
                    text=MANAGE_PROMOS, callback_data="seller_promo_list_menu"
                )
            ],
            [
                InlineKeyboardButton(
                    text=PUBLISH_PROMO, callback_data="publish_product_promo"
                )
            ],
            [InlineKeyboardButton(text=MAIN_MENU, callback_data="back_to_start")],
        ]
    )


def get_promo_detailview_keyboard(promo_id: str, status: bool) -> InlineKeyboardMarkup:
    inline_keyboard = []
    action = "d" if status == "active" else "a"
    if status == "active":
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=DEACTIVATE,
                    callback_data=f"promo_status:{promo_id}:{action}",
                )
            ]
        )
    else:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=ACTIVATE,
                    callback_data=f"promo_status:{promo_id}:{action}",
                )
            ]
        )
    inline_keyboard.append(
        [InlineKeyboardButton(text=EDIT_PROMO, callback_data=f"edit_promo:{promo_id}")]
    )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=DELETE_PROMO, callback_data=f"delete_promo:{promo_id}"
            )
        ],
    )

    inline_keyboard.append(
        [InlineKeyboardButton(text=BACK, callback_data="seller_promo_list_menu")]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_confirm_toggle_promo_status_keyboard(promo_id, action):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=CONFIRM,
                    callback_data=f"confirm_toggle_promo:{promo_id}:{action}",
                ),
                InlineKeyboardButton(
                    text=CANCEL, callback_data=f"cancel_toggle_promo:{promo_id}"
                ),
            ]
        ]
    )


def get_edit_promo_keyboard(
    promo_id: str, PROMO_FIELD_LABELS: dict
) -> InlineKeyboardMarkup:
    buttons = []
    for item in PROMO_FIELD_LABELS:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=PROMO_FIELD_LABELS[item],
                    callback_data=f"edit_promo_field:{item}",
                )
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text=CANCEL,
                callback_data=f"promo_details_menu:{promo_id}",
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_abort_edit_promo_field_keyboard(promo_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=CANCEL, callback_data=f"edit_promo:{promo_id}"
                ),
            ]
        ]
    )


def get_confirm_edit_promo_keyboard(promo_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=SAVE, callback_data=f"confirm_edit_promo:{promo_id}"
                )
            ],
            [InlineKeyboardButton(text=CANCEL, callback_data="cancel_edit_promo")],
        ]
    )


def get_back_to_promo_detailview_keyboard(promo_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BACK, callback_data=f"promo_detail_menu:{promo_id}"
                )
            ]
        ]
    )


def get_confirm_delete_promo_keyboard(promo_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=CONFIRM_DELETE,
                    callback_data="confirm_delete_promo",
                ),
                InlineKeyboardButton(
                    text=CANCEL,
                    callback_data=f"cancel_delete_promo:{promo_id}",
                ),
            ]
        ]
    )

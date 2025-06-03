from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_abort_create_seller_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Abbrechen", callback_data="admin_sellers_menu"
                ),
            ],
        ]
    )


def get_manage_sellers_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Verkäufer hinzufügen",
                    callback_data="add_seller",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📃 Verkäuferliste", callback_data="seller_list_menu"
                )
            ],
            [InlineKeyboardButton(text="🔙 Hauptmenu", callback_data="back_to_start")],
        ]
    )


def get_seller_details_menu_keyboard(
    telegram_id: int, status: str
) -> InlineKeyboardMarkup:
    inline_keyboard = []

    if status == "active":
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="🚫 Deaktivieren",
                    callback_data=f"seller_toggle_is_active:{telegram_id}:deactivate",
                )
            ]
        )
    elif status == "inactive":
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="✅ Aktivieren",
                    callback_data=f"seller_toggle_is_active:{telegram_id}:activate",
                )
            ]
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🗑 Verkäufer löschen",
                callback_data=f"seller_delete:{telegram_id}",
            )
        ]
    )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔙 Zurück zur Übersicht",
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
                    text="✅ Ja",
                    callback_data=f"confirm_toggle_seller_is_active:{telegram_id}:{action}",
                ),
                InlineKeyboardButton(
                    text="❌ Abbrechen",
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
                    text="✅ Ja, löschen",
                    callback_data=f"seller_delete_confirm:{telegram_id}",
                ),
                InlineKeyboardButton(
                    text="❌ Abbrechen",
                    callback_data=f"cancel_delete_seller:{telegram_id}",
                ),
            ]
        ]
    )


def get_seller_list_keyboard(sellers: list[dict]) -> InlineKeyboardMarkup:
    buttons = []

    for seller in sellers:
        telegram_id = seller.get("telegram_user_id")
        display_name = seller.get("display_name")
        button_text = f"👤 {display_name}" if display_name else f"🆔 {telegram_id}"
        buttons.append(
            [
                InlineKeyboardButton(
                    text=button_text, callback_data=f"seller_details_menu:{telegram_id}"
                )
            ]
        )

    buttons.append(
        [InlineKeyboardButton(text="🔙 Hauptmenu", callback_data="back_to_start")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_retry_or_abort_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Eingabe wiederholen", callback_data="add_seller"
                )
            ],
            [InlineKeyboardButton(text="🔙 Hauptmenu", callback_data="back_to_start")],
        ]
    )

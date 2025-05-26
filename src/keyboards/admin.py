from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_admin_keyboard():
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
                    text="📃 Verkäuferliste", callback_data="display_sellers"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📣 Angebote", callback_data="display_promotions"
                )
            ],
            [InlineKeyboardButton(text="↩️ Neustart", callback_data="back_to_start")],
        ]
    )


def get_seller_detail_keyboard(telegram_id: int, active: bool) -> InlineKeyboardMarkup:
    inline_keyboard = []

    if active:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="🚫 Deaktivieren",
                    callback_data=f"seller_toggle:{telegram_id}:deactivate",
                )
            ]
        )
    else:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="✅ Aktivieren",
                    callback_data=f"seller_toggle:{telegram_id}:activate",
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
                callback_data="display_sellers",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_confirm_toggle_keyboard(telegram_id, action):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Ja", callback_data=f"confirm_toggle:{telegram_id}:{action}"
                ),
                InlineKeyboardButton(
                    text="❌ Abbrechen", callback_data=f"cancel_toggle:{telegram_id}"
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
                    text=button_text, callback_data=f"seller_detail:{telegram_id}"
                )
            ]
        )

    buttons.append(
        [InlineKeyboardButton(text="🔙 Zurück", callback_data="back_to_start")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)

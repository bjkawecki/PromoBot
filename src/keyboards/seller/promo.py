from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_confirm_create_promo_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Bestätigen",
                    callback_data="confirm_create_promo",
                ),
                InlineKeyboardButton(
                    text="❌ Abbrechen", callback_data="back_to_start"
                ),
            ]
        ]
    )


def get_promo_list_keyboard(promo_list: list[dict]) -> InlineKeyboardMarkup:
    buttons = []

    for promo in promo_list:
        promo_id = promo.get("promo_id")
        display_name = promo.get("display_name")
        button_text = f" {display_name}"
        buttons.append(
            [
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"promo_detail:{promo_id}",
                )
            ]
        )

    buttons.append(
        [InlineKeyboardButton(text="🔙 Zurück", callback_data="back_to_start")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_inline_keyboard(link) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Jetzt bestellen",
                    url=link,
                )
            ]
        ]
    )
    return keyboard


def get_promo_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Promo erstellen", callback_data="create_promo"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📁 Promos verwalten", callback_data="get_seller_promos"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨 Promo senden", callback_data="send_product_promo"
                )
            ],
            [InlineKeyboardButton(text="🔙 Zurück", callback_data="back_to_start")],
        ]
    )


def get_promo_detailview_keyboard(
    promo_id: str, is_active: bool
) -> InlineKeyboardMarkup:
    inline_keyboard = []
    action = "d" if is_active else "a"
    if is_active:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="🚫 Deaktivieren",
                    callback_data=f"promo_status:{promo_id}:{action}",
                )
            ]
        )
    else:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="✅ Aktivieren",
                    callback_data=f"promo_status:{promo_id}:{action}",
                )
            ]
        )
    inline_keyboard.append(
        [InlineKeyboardButton(text="Promo bearbeiten", callback_data="update_promo")]
    )

    inline_keyboard.append(
        [InlineKeyboardButton(text="Promo löschen", callback_data="delete_promo")],
    )

    inline_keyboard.append(
        [InlineKeyboardButton(text="Zurück", callback_data="get_seller_promos")]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_confirm_toggle_promo_status_keyboard(promo_id, action):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Bestätigen",
                    callback_data=f"confirm_toggle_promo:{promo_id}:{action}",
                ),
                InlineKeyboardButton(
                    text="❌ Abbrechen",
                    callback_data=f"cancel_toggle_promo:{promo_id}",
                ),
            ]
        ]
    )

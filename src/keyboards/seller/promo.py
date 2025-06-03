from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_back_to_promo_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Abbrechen", callback_data="promo_menu")]
        ]
    )


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
                    callback_data=f"promo_detail_menu:{promo_id}",
                )
            ]
        )

    buttons.append([InlineKeyboardButton(text="🔙 Zurück", callback_data="promo_menu")])

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
                    text="📁 Promos verwalten", callback_data="seller_promo_list_menu"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨 Promo veröffentlichen",
                    callback_data="publish_product_promo",
                )
            ],
            [InlineKeyboardButton(text="🔙 Zurück", callback_data="back_to_start")],
        ]
    )


def get_promo_detailview_keyboard(promo_id: str, status: bool) -> InlineKeyboardMarkup:
    inline_keyboard = []
    action = "d" if status == "active" else "a"
    if status == "active":
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
                    text="🔛 Aktivieren",
                    callback_data=f"promo_status:{promo_id}:{action}",
                )
            ]
        )
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="Promo bearbeiten", callback_data=f"edit_promo:{promo_id}"
            )
        ]
    )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="Promo löschen", callback_data=f"delete_promo:{promo_id}"
            )
        ],
    )

    inline_keyboard.append(
        [InlineKeyboardButton(text="Zurück", callback_data="seller_promo_list_menu")]
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
                text="❌ Abbrechen",
                callback_data=f"promo_detail_menu:{promo_id}",
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_abort_edit_promo_field_keyboard(promo_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Abbrechen", callback_data=f"edit_promo:{promo_id}"
                ),
            ]
        ]
    )


def get_confirm_edit_promo_keyboard(promo_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Speichern", callback_data=f"confirm_edit_promo:{promo_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Abbrechen", callback_data="cancel_edit_promo"
                )
            ],
        ]
    )


def get_back_to_promo_detailview_keyboard(promo_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Zurück", callback_data=f"promo_detail_menu:{promo_id}"
                )
            ]
        ]
    )


def get_confirm_delete_promo_keyboard(promo_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Ja, löschen",
                    callback_data="confirm_delete_promo",
                ),
                InlineKeyboardButton(
                    text="❌ Abbrechen",
                    callback_data=f"cancel_delete_promo:{promo_id}",
                ),
            ]
        ]
    )

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
                    text=button_text, callback_data=f"promo_detail:{promo_id}"
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

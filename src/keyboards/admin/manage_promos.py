from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_admin_promo_detailview_keyboard(promo_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Zurück", callback_data="admin_promo_list_menu")]
        ]
    )


def get_admin_promo_list_keyboard(promo_list: list[dict]) -> InlineKeyboardMarkup:
    buttons = []

    for promo in promo_list:
        promo_id = promo.get("promo_id")
        display_name = promo.get("display_name")
        promo_status = promo.get("promo_status")
        button_text = f"{display_name}\n{promo_status}"
        buttons.append(
            [
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"admin_promo_details_menu:{promo_id}",
                )
            ]
        )

    buttons.append(
        [InlineKeyboardButton(text="🔙 Zurück", callback_data="back_to_start")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.misc import promo_status_emoji_map


def get_admin_promo_detailview_keyboard(promo_status: str) -> InlineKeyboardMarkup:
    buttons = []
    if promo_status == "deleted":
        buttons.append(
            [
                InlineKeyboardButton(
                    text="💥 Endgültig löschen",
                    callback_data="admin_hard_delete_promo",
                )
            ]
        )
    else:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="🗑 Als gelöscht markieren",
                    callback_data="admin_soft_delete_promo",
                )
            ]
        )

    buttons.append(
        [InlineKeyboardButton(text="🔙 Zurück", callback_data="admin_promo_list_menu")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_promo_list_keyboard(promo_list: list[dict]) -> InlineKeyboardMarkup:
    buttons = []

    for promo in promo_list:
        promo_id = promo.get("promo_id")
        display_name = promo.get("display_name")
        promo_status = promo_status_emoji_map[promo.get("promo_status")]
        button_text = f"{display_name}\n\n{promo_status}"
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


def get_confirm_hard_delete_promo_keyboard(promo_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Ja, löschen",
                    callback_data="confirm_hard_delete_promo",
                ),
                InlineKeyboardButton(
                    text="❌ Abbrechen",
                    callback_data=f"cancel_delete_promo:{promo_id}",
                ),
            ]
        ]
    )


def get_confirm_soft_delete_promo_keyboard(promo_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Ja",
                    callback_data="confirm_soft_delete_promo",
                ),
                InlineKeyboardButton(
                    text="❌ Abbrechen",
                    callback_data=f"cancel_delete_promo:{promo_id}",
                ),
            ]
        ]
    )

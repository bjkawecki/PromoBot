from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.admin.start import get_admin_keyboard
from keyboards.buyer.start import get_buyer_keyboard
from keyboards.seller.start import (
    get_active_registered_seller_keyboard,
    get_inactive_registered_seller_keyboard,
    get_unregistered_seller_keyboard,
)


def get_abort_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Abbrechen", callback_data="back_to_start"),
            ],
        ]
    )


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Hauptmenü", callback_data="back_to_start")]
        ]
    )


def get_role_keyboard(role: str, seller) -> InlineKeyboardMarkup:
    if role == "admin":
        return get_admin_keyboard
    elif role == "seller":
        if seller.get("is_registered", False):
            if seller.get("seller_status") == "active":
                return get_active_registered_seller_keyboard
            else:
                return get_inactive_registered_seller_keyboard
        return get_unregistered_seller_keyboard
    else:
        return get_buyer_keyboard


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
                    callback_data=f"promo_details_menu:{promo_id}",
                )
            ]
        )

    buttons.append([InlineKeyboardButton(text="🔙 Zurück", callback_data="promo_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

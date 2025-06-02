from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.repositories.sellers import get_all_sellers, get_seller_by_id
from keyboards.admin.manage_seller import (
    get_seller_details_menu_keyboard,
    get_seller_list_keyboard,
)
from utils.misc import get_seller_info

router = Router()


@router.callback_query(F.data == "seller_list_menu")
async def seller_list_menu_callback(callback: CallbackQuery):
    seller_list = get_all_sellers()

    if not seller_list:
        await callback.answer("❌ Es sind noch keine Verkäufer registriert.")
        return

    keyboard = get_seller_list_keyboard(seller_list)
    await callback.message.edit_text(
        "Wähle einen Verkäufer aus:", reply_markup=keyboard
    )
    await callback.answer()


@router.callback_query(F.data.startswith("seller_details_menu:"))
async def seller_details_menu_callback(callback: CallbackQuery):
    print(f"DEBUG: callback.data = {repr(callback.data)}")

    telegram_id = callback.data.split(":")[1]

    seller = get_seller_by_id(int(telegram_id))
    if not seller:
        await callback.message.answer("Verkäufer nicht gefunden.")
        return

    seller_info = get_seller_info(seller)

    keyboard = get_seller_details_menu_keyboard(
        telegram_id, seller.get("active", False)
    )

    await callback.message.edit_text(
        seller_info, reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()

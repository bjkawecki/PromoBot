from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.repositories.promos import get_promotions_by_seller_id
from database.repositories.sellers import get_all_sellers, get_seller_by_id
from keyboards.admin.manage_promos import get_admin_promo_list_keyboard
from keyboards.admin.manage_seller import (
    get_manage_sellers_menu_keyboard,
    get_seller_details_menu_keyboard,
    get_seller_list_keyboard,
)
from utils.misc import get_seller_info

router = Router()


@router.callback_query(F.data == "admin_sellers_menu")
async def admin_seller_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>👔 Verkäufer-Menü</b>",
        reply_markup=get_manage_sellers_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


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
    telegram_id = callback.data.split(":")[1]
    seller = get_seller_by_id(int(telegram_id))
    if not seller:
        await callback.message.answer("Verkäufer nicht gefunden.")
        return

    seller_info = get_seller_info(seller)

    keyboard = get_seller_details_menu_keyboard(
        telegram_id, seller.get("seller_status")
    )

    await callback.message.edit_text(
        seller_info, reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin_seller_promo_list:"))
async def seller_promo_list_menu_callback(callback: CallbackQuery):
    telegram_id = callback.data.split(":")[1]
    promo_list = get_promotions_by_seller_id(seller_id=int(telegram_id))

    if not promo_list:
        await callback.answer("❌ Verkäufer hat noch keine Promos erstellt.")
        return
    keyboard = get_admin_promo_list_keyboard(promo_list)
    await callback.message.answer(
        "<b>📢 Promos</b>\n\nWähle eine Promo aus:",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()

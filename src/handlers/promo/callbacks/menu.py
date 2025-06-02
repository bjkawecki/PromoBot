from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.repositories.promos import get_promo_by_id, get_promotions_by_seller_id
from keyboards.seller.promo import (
    get_promo_detailview_keyboard,
    get_promo_list_keyboard,
    get_promo_menu_keyboard,
)
from utils.misc import get_promo_details

router = Router()


@router.callback_query(F.data == "promo_menu")
async def promo_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>📢 Promo-Menu</b>",
        reply_markup=get_promo_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "seller_promo_list_menu")
async def seller_promo_list_menu_callback(callback: CallbackQuery, state: FSMContext):
    seller_id = callback.from_user.id
    promo_list = get_promotions_by_seller_id(seller_id)
    if not promo_list:
        await callback.answer("❌ Du hast noch keine Promo erstellt.")
        return
    keyboard = get_promo_list_keyboard(promo_list)
    await callback.message.edit_text("Wähle eine Promo aus:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("promo_detail_menu:"))
async def promo_detailview_callback(callback: CallbackQuery):
    seller_id = callback.from_user.id
    promo_id = callback.data.split(":")[1]

    promo = get_promo_by_id(promo_id, seller_id)

    if not promo:
        await callback.answer("Promo nicht gefunden.")
        return
    status = promo.get("status", False)
    promo_details = get_promo_details(promo)

    keyboard = get_promo_detailview_keyboard(promo_id, status)

    await callback.message.answer(
        promo_details, reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()

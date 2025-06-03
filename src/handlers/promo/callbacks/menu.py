from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.repositories.promos import get_promo_by_id, get_promotions_by_seller_id
from handlers.promo.message_handlers.menu import send_promo_detailview
from keyboards.seller.promo import (
    get_promo_list_keyboard,
    get_promo_menu_keyboard,
)

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
        await callback.answer("❌ Du hast noch keine Promos erstellt.")
        return
    keyboard = get_promo_list_keyboard(promo_list)
    await callback.message.answer("Wähle eine Promo aus:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("promo_detail_menu:"))
async def promo_details_menu_callback(callback: CallbackQuery, state: FSMContext):
    seller_id = callback.from_user.id
    promo_id = callback.data.split(":")[1]
    promo = get_promo_by_id(promo_id, seller_id)
    await state.update_data(display_name=promo.get("display_name"))
    if not promo:
        await callback.answer("Promo nicht gefunden.")
        return
    await send_promo_detailview(callback.message, promo)
    await callback.answer()

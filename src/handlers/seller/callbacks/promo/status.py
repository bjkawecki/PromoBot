from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.repositories.promos import get_promo_by_promo_id_and_seller_id, save_promo
from handlers.seller.callbacks.promo.menu import seller_promo_list_menu_callback
from keyboards.seller.promo import get_confirm_toggle_promo_status_keyboard
from messages.common.info import PROCESS_ABORTED
from messages.common.promo import PROMO_NOT_FOUND
from messages.seller.promo import confirm_toggle_promo_status, confirm_toggled_promo

router = Router()


@router.callback_query(F.data.startswith("promo_status:"))
async def toggle_promo_status_callback(callback: CallbackQuery):
    _, promo_id, action = callback.data.split(":")
    keyboard = get_confirm_toggle_promo_status_keyboard(promo_id, action)
    await callback.message.answer(
        confirm_toggle_promo_status(action), reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_toggle_promo"))
async def cancel_toggle_callback(callback: CallbackQuery):
    await callback.answer(PROCESS_ABORTED)
    await seller_promo_list_menu_callback(callback)


@router.callback_query(F.data.startswith("confirm_toggle_promo:"))
async def confirm_toggle_callback(callback: CallbackQuery, state: FSMContext):
    seller_id = callback.from_user.id
    _, promo_id, action = callback.data.split(":")
    promo = get_promo_by_promo_id_and_seller_id(promo_id=promo_id, seller_id=seller_id)
    if not promo:
        await callback.message.answer(PROMO_NOT_FOUND)
        return
    promo["promo_status"] = "active" if action == "a" else "inactive"
    save_promo(promo)
    confirm_toggle_promo_status(promo["promo_status"])
    await callback.answer(confirm_toggled_promo(promo["promo_status"]))
    await seller_promo_list_menu_callback(callback, state)
    await callback.answer()

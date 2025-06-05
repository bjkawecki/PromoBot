from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.repositories.promos import set_promo_status_to_deleted
from handlers.seller.callbacks.promo.menu import promo_details_menu_callback
from keyboards.seller.promo import (
    get_confirm_delete_promo_keyboard,
    get_promo_menu_keyboard,
)
from messages.admin.delete import delete_error_message
from messages.common.info import (
    ERROR_PROCESSING_REQUEST,
    PROCESS_ABORTED,
    confirm_soft_deleted_promo,
    error_detele_promo,
)
from messages.common.promo import confirm_soft_delete_promo_message

router = Router()


@router.callback_query(F.data.startswith("delete_promo:"))
async def delete_promo_callback(callback: CallbackQuery, state: FSMContext):
    try:
        _, promo_id = callback.data.split(":", 1)  # Falls mehr ":" enthalten sind
        data = await state.get_data()
        promo_name = data.get("display_name", "Unbekannte Promo")  # Fallback
        # promo_id im State speichern für spätere Bestätigung
        await state.update_data(promo_id=promo_id)
        await callback.message.answer(
            confirm_soft_delete_promo_message(promo_name),
            reply_markup=get_confirm_delete_promo_keyboard(promo_id),
            parse_mode="HTML",
        )
        await callback.answer()
    except Exception as e:
        print(error_detele_promo(e))
        await callback.answer(ERROR_PROCESSING_REQUEST, show_alert=True)


@router.callback_query(F.data.startswith("cancel_delete_promo:"))
async def cancel_delete_seller_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer(PROCESS_ABORTED)
    await promo_details_menu_callback(callback, state)
    await callback.answer()


@router.callback_query(F.data == "confirm_delete_promo")
async def confirm_delete_promo_callback(callback: CallbackQuery, state: FSMContext):
    seller_id = callback.from_user.id
    data = await state.get_data()
    promo_id = data.get("promo_id", "")
    data = await state.get_data()
    promo_name = data.get("display_name")
    try:
        set_promo_status_to_deleted(promo_id, seller_id)
        await callback.message.edit_text(
            confirm_soft_deleted_promo(promo_name),
            reply_markup=get_promo_menu_keyboard(),
        )
    except Exception as e:
        await callback.message.edit_text(delete_error_message(e))

    await callback.answer()
    await state.clear()

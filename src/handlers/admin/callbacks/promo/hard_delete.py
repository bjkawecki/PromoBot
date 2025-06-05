from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.repositories.promos import hard_delete_promo
from keyboards.admin.manage_promos import get_confirm_hard_delete_promo_keyboard
from keyboards.common import get_main_menu_keyboard
from messages.admin.delete import (
    confirm_delete_promo_message,
    delete_error_message,
    promo_deleted_message,
)

router = Router()


@router.callback_query(F.data == "admin_hard_delete_promo")
async def admin_hard_delete_promo_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    promo = data.get("promo")
    display_name = promo.get("display_name")
    promo_id = promo.get("promo_id")
    keyboard = get_confirm_hard_delete_promo_keyboard(promo_id)

    await callback.message.answer(
        confirm_delete_promo_message(display_name),
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "confirm_hard_delete_promo")
async def seller_delete_execute(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    promo = data.get("promo")
    seller_id = promo.get("seller_id")
    promo_id = promo.get("promo_id")
    display_name = promo.get("display_name")

    try:
        _ = hard_delete_promo(promo_id, seller_id)
        if _:
            await callback.message.edit_text(
                promo_deleted_message(display_name),
                reply_markup=get_main_menu_keyboard(),
            )
        else:
            raise Exception
    except Exception as e:
        await callback.message.edit_text(delete_error_message(e))
    await state.clear()
    await callback.answer()

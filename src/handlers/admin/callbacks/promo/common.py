from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.admin.callbacks.promo.menu import admin_promo_details_menu_callback
from messages.common.info import PROCESS_ABORTED

router = Router()


@router.callback_query(F.data.startswith("cancel_delete_promo:"))
async def cancel_hard_delete_promo_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer(PROCESS_ABORTED)
    await admin_promo_details_menu_callback(callback, state)
    await callback.answer()

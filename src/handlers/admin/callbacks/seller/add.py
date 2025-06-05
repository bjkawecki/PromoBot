from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import ADMIN_USER_NAME
from keyboards.admin.manage_seller import get_abort_create_seller_keyboard
from messages.admin.seller import ADD_NEW_SELLER_MESSAGE
from messages.common.info import NOT_AUTHORIZED_ANSWER
from states.admin import AddSeller

router = Router()


@router.callback_query(F.data == "add_seller")
async def add_seller_callback(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.username != ADMIN_USER_NAME:
        await callback.answer(NOT_AUTHORIZED_ANSWER, show_alert=True)
        return

    await callback.message.edit_text(
        ADD_NEW_SELLER_MESSAGE,
        parse_mode="HTML",
        reply_markup=get_abort_create_seller_keyboard(),
    )
    await callback.answer()
    await state.set_state(AddSeller.waiting_for_seller_telegram_id)

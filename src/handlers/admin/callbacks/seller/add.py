from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import ADMIN_USER_NAME
from keyboards.admin.manage_seller import get_abort_create_seller_keyboard
from states.admin import AddSeller

router = Router()


@router.callback_query(F.data == "add_seller")
async def add_seller_callback(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.username != ADMIN_USER_NAME:
        await callback.answer("Keine Berechtigung.", show_alert=True)
        return

    await callback.message.edit_text(
        "Neuen Verkäufer hinzufügen\n\n"
        "Bitte gib die *Telegram\\-Nutzer\\-ID* des neuen Verkäufers an:",
        parse_mode="MarkdownV2",
        reply_markup=get_abort_create_seller_keyboard(),
    )
    await callback.answer()
    await state.set_state(AddSeller.waiting_for_seller_telegram_id)

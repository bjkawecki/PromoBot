from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.start import get_main_menu_deeplink
from messages.welcome_text import welcome_text

router = Router()


@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()  # FSM Zustand zurücksetzen
    await callback.message.edit_text("🚫 Bestellung abgebrochen.")

    # Optional: Zurück zum Startmenü
    await callback.message.answer(
        welcome_text,
        reply_markup=get_main_menu_deeplink(),
        parse_mode="MarkdownV2",
    )

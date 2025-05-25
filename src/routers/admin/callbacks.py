# callbacks/admin.py


from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import ADMIN_USER_NAME
from routers.admin.states import AddSeller

router = Router()


@router.callback_query(F.data == "add_seller")
async def add_seller_callback(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.username != ADMIN_USER_NAME:
        await callback.answer("Keine Berechtigung.", show_alert=True)
        return

    await callback.message.answer(
        "*Neuer Verkäufer hinzufügen*\n\n"
        "Bitte sende die Telegram\\-Nutzer\\-ID des neuen Verkäufers:",
        parse_mode="MarkdownV2",
    )
    await callback.answer()
    await state.set_state(AddSeller.waiting_for_username)

from datetime import datetime

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from database.repositories.sellers import save_seller
from keyboards.admin import admin_keyboard
from routers.admin.states import AddSeller

router = Router()


@router.message(AddSeller.waiting_for_username)
async def save_seller_username(message: types.Message, state: FSMContext):
    telegram_user_id = message.text.strip()
    telegram_user_id = int(telegram_user_id)
    seller_obj = {
        "telegram_user_id": telegram_user_id,
        "active": True,
        "registered": False,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    save_seller(seller_obj)

    await message.answer(
        f"✅ Neuer Verkäufer mit Telegram-User-ID {telegram_user_id} wurde gespeichert.",
        reply_markup=admin_keyboard(),
    )
    await state.clear()

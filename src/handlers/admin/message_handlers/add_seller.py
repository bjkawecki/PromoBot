from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.repositories.sellers import save_seller
from keyboards.admin.start import get_admin_keyboard
from states.admin import AddSeller
from utils.validation import validate_telegram_user_id

router = Router()


@router.message(AddSeller.waiting_for_seller_telegram_id)
async def save_seller_telegram_id(message: Message, state: FSMContext):
    telegram_user_id = await validate_telegram_user_id(message, message.text)
    if not telegram_user_id:
        return
    telegram_user_id = message.text.strip()
    telegram_user_id = int(telegram_user_id)
    seller_obj = {
        "telegram_user_id": telegram_user_id,
        "status": "active",
        "registered": False,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    save_seller(seller_obj)

    await message.answer(
        f"✅ Neuer Verkäufer mit Telegram-User-ID {telegram_user_id} wurde gespeichert.",
        reply_markup=get_admin_keyboard(),
    )
    await state.clear()

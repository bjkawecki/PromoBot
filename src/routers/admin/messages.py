import json
from datetime import datetime

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from config import seller_table
from routers.admin.states import AddSeller

router = Router()


@router.message(AddSeller.waiting_for_username)
async def save_seller_username(message: types.Message, state: FSMContext):
    telegram_user_id = int(message.text.strip())
    print(telegram_user_id)
    seller_obj = {
        "telegram_user_id": telegram_user_id,
        "active": True,
        "registered": False,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    seller_table.put_item(Item=seller_obj)

    await message.answer(f"✅ {telegram_user_id} wurde als Verkäufer gespeichert.")
    await state.clear()

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.admin import admin_keyboard
from keyboards.buyer import buyer_keyboard
from keyboards.seller import seller_keyboard

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, role: str):
    print("Rolle:", role)
    if role == "admin":
        await message.answer("Willkommen, Admin!", reply_markup=admin_keyboard())
    elif role == "seller":
        await message.answer("Hallo Verkäufer!", reply_markup=seller_keyboard())
    else:
        await message.answer("Willkommen, Kunde!", reply_markup=buyer_keyboard())

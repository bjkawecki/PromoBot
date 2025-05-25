from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards.common import get_role_keyboard
from messages.welcome_text import get_role_welcome_message_text

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, role: str):
    print("Rolle:", role)
    role_keyboard = get_role_keyboard(role)
    role_welcome_message = get_role_welcome_message_text(role)
    await message.answer(role_welcome_message, reply_markup=role_keyboard())


@router.callback_query(F.data == "back_to_start")
async def back_to_start_callback(callback: CallbackQuery, role: str):
    role_keyboard = get_role_keyboard(role)
    role_welcome_message = get_role_welcome_message_text(role)
    await callback.message.answer(
        role_welcome_message,
        reply_markup=role_keyboard(),
    )
    await callback.answer()

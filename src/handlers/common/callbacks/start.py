from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards.common import get_role_keyboard
from messages.common.start import get_role_welcome_message_text

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, role: str, seller):
    role_keyboard = get_role_keyboard(role, seller)
    role_welcome_message = get_role_welcome_message_text(role, seller)
    await message.answer(
        role_welcome_message, reply_markup=role_keyboard(), parse_mode="HTML"
    )


@router.callback_query(F.data == "back_to_start")
async def back_to_start_callback(callback: CallbackQuery, role: str, seller):
    role_keyboard = get_role_keyboard(role, seller)
    role_welcome_message = get_role_welcome_message_text(role, seller)
    await callback.message.edit_text(
        role_welcome_message, reply_markup=role_keyboard(), parse_mode="HTML"
    )
    await callback.answer()

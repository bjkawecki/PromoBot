from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.start import get_main_menu_deeplink
from messages.welcome_text import welcome_text

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        welcome_text, reply_markup=get_main_menu_deeplink(), parse_mode="MarkdownV2"
    )

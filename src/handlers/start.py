from aiogram import F, Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards.start import get_main_menu_deeplink
from messages.welcome_text import welcome_text
from messages.welcome_text import welcome_text as default_welcome_text

router = Router()


@router.message(CommandStart(deep_link=True))
async def cmd_start_deep(message: Message, command: CommandObject):
    payload = command.args
    if payload:
        welcome_text = f"Wie ich sehe, nimmst du an Promo\\-Aktion {payload} teil\."
    else:
        welcome_text = default_welcome_text
    await message.answer(
        welcome_text, reply_markup=get_main_menu_deeplink(), parse_mode="MarkdownV2"
    )


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        welcome_text, reply_markup=get_main_menu_deeplink(), parse_mode="MarkdownV2"
    )


@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery):
    await callback.message.answer(
        welcome_text,
        reply_markup=get_main_menu_deeplink(),
        parse_mode="MarkdownV2",
    )
    await callback.answer()

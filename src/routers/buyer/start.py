from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.start import get_main_menu_deeplink
from messages.welcome_text import welcome_text

router = Router()


@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery):
    await callback.message.answer(
        welcome_text,
        reply_markup=get_main_menu_deeplink(),
        parse_mode="MarkdownV2",
    )
    await callback.answer()

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from config import verkaeufer_kanal_id
from keyboards.inline import get_inline_keyboard

router = Router()


@router.callback_query(F.data == "send_product_promo")
async def send_product_promo(callback: CallbackQuery, bot):
    link = await create_start_link(bot, "PROMO1")

    await bot.send_message(
        chat_id=verkaeufer_kanal_id,
        text="Unser neues Produkt XY! Bestelle jetzt bequem hier:",
        reply_markup=get_inline_keyboard(link),
    )
    await callback.answer()  # Feedback im UI

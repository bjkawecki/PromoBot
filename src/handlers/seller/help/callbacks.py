from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.seller.help import (
    get_back_to_seller_help_menu_keyboard,
    get_seller_help_menu_keyboard,
)
from messages.seller import HELP_TOPICS

router = Router()


@router.callback_query(lambda c: c.data == "seller_help_menu")
async def seller_help_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>❓ Hilfe zur Nutzung von PromoBot</b>\n\nDrück auf das Thema, über das du mehr erfahren möchtest.",
        reply_markup=get_seller_help_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("seller_help:"))
async def seller_help_callback(callback: CallbackQuery):
    _, topic = callback.data.split(":")
    text = HELP_TOPICS.get(topic, "Dieses Hilfethema existiert leider nicht.")

    await callback.message.edit_text(
        text=text,
        reply_markup=get_back_to_seller_help_menu_keyboard(),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

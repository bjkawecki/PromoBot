from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.common import get_main_menu_keyboard
from keyboards.help import get_back_to_help_options_keyboard, get_help_options_keyboard
from messages.help import (
    data_privacy_text,
    how_to_get_order_status_text,
    how_to_order_text,
)

router = Router()


@router.callback_query(F.data == "display_bot_help_options")
async def display_bot_help_options(callback: CallbackQuery):
    await callback.message.answer(
        "*❓ Hilfe zur Nutzung von PromoBot*\n\nDrück auf das Thema, über das du mehr erfahren möchtest\\.",
        reply_markup=get_help_options_keyboard(),
        parse_mode="MarkdownV2",
    )
    await callback.answer()


@router.callback_query(F.data == "how_to_order")
async def how_to_order(callback: CallbackQuery):
    await callback.message.answer(
        how_to_order_text,
        reply_markup=get_back_to_help_options_keyboard(),
        parse_mode="MarkdownV2",
    )
    await callback.answer()


@router.callback_query(F.data == "how_to_get_order_status")
async def how_to_get_order_status(callback: CallbackQuery):
    await callback.message.answer(
        how_to_get_order_status_text,
        reply_markup=get_back_to_help_options_keyboard(),
        parse_mode="MarkdownV2",
    )
    await callback.answer()


@router.callback_query(F.data == "data_privacy")
async def data_privacy(callback: CallbackQuery):
    await callback.message.answer(
        data_privacy_text,
        reply_markup=get_back_to_help_options_keyboard(),
        parse_mode="MarkdownV2",
    )
    await callback.answer()


@router.callback_query(F.data == "display_product_description")
async def display_product_description(callback: CallbackQuery):
    await callback.message.answer(
        "*🔍 Produktbeschreibung*\n\n_Hier kann man mehr über das beworbene Produkt erfahren\\._",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="MarkdownV2",
    )
    await callback.answer()

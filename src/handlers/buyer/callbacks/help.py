from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.buyer.help import (
    get_back_to_help_options_keyboard,
    get_help_options_keyboard,
)
from messages.buyer.help import (
    buyer_help_menu_message,
    data_privacy_text,
    how_to_get_order_status_text,
    how_to_order_text,
)

router = Router()


@router.callback_query(F.data == "display_bot_help_options")
async def display_bot_help_options(callback: CallbackQuery):
    await callback.message.answer(
        buyer_help_menu_message,
        reply_markup=get_help_options_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "how_to_order")
async def how_to_order(callback: CallbackQuery):
    await callback.message.answer(
        how_to_order_text,
        reply_markup=get_back_to_help_options_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "how_to_get_order_status")
async def how_to_get_order_status(callback: CallbackQuery):
    await callback.message.answer(
        how_to_get_order_status_text,
        reply_markup=get_back_to_help_options_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "data_privacy")
async def data_privacy(callback: CallbackQuery):
    await callback.message.answer(
        data_privacy_text,
        reply_markup=get_back_to_help_options_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()

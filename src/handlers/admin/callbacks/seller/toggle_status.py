from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.repositories.sellers import get_seller_by_id, save_seller
from handlers.admin.callbacks.seller.menu import seller_details_menu_callback
from keyboards.admin.manage_seller import get_confirm_toggle_keyboard
from messages.admin.seller import (
    SELLER_NOT_FOUND,
    confirm_seller_toggle_answer,
    confirm_toggle_user_message,
    format_seller_info,
)
from messages.common.info import PROCESS_ABORTED

router = Router()


@router.callback_query(F.data.startswith("seller_toggle_is_active:"))
async def seller_toggle_is_active_callback(callback: CallbackQuery):
    _, telegram_id, action = callback.data.split(":")
    seller = get_seller_by_id(int(telegram_id))
    seller_info = format_seller_info(seller)
    confirm_toggle_user_message(action, seller_info)
    keyboard = get_confirm_toggle_keyboard(telegram_id, action)
    await callback.message.edit_text(
        confirm_toggle_user_message(action, seller_info),
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_toggle_seller_is_active"))
async def cancel_toggle_callback(callback: CallbackQuery):
    await callback.answer(PROCESS_ABORTED)
    await seller_details_menu_callback(callback)
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_toggle_seller_is_active:"))
async def confirm_toggle_callback(callback: CallbackQuery):
    _, telegram_id, action = callback.data.split(":")

    seller = get_seller_by_id(int(telegram_id))
    if not seller:
        await callback.message.answer(SELLER_NOT_FOUND)
        return
    seller["seller_status"] = "active" if action == "activate" else "inactive"
    save_seller(seller)
    await callback.answer(confirm_seller_toggle_answer(seller["seller_status"]))
    await seller_details_menu_callback(callback)
    await callback.answer()

from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.repositories.sellers import delete_seller_by_id, get_seller_by_id
from handlers.admin.callbacks.seller.menu import seller_details_menu_callback
from keyboards.admin.manage_seller import (
    get_confirm_delete_seller_keyboard,
)
from keyboards.common import get_main_menu_keyboard
from messages.admin.delete import (
    confirm_delete_seller_message,
    delete_error_message,
    delete_seller_not_possible_message,
    deleted_seller_confirm_message,
)
from messages.admin.seller import format_seller_info, seller_not_found_answer
from messages.common.info import PROCESS_ABORTED

router = Router()


@router.callback_query(F.data.startswith("seller_delete:"))
async def seller_delete_confirm(callback: CallbackQuery):
    _, telegram_id = callback.data.split(":")
    seller = get_seller_by_id(int(telegram_id))
    seller_info = format_seller_info(seller)
    keyboard = get_confirm_delete_seller_keyboard(telegram_id)

    await callback.message.edit_text(
        confirm_delete_seller_message(seller_info),
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_delete_seller"))
async def cancel_delete_seller_callback(callback: CallbackQuery):
    await callback.answer(PROCESS_ABORTED)
    await seller_details_menu_callback(callback)
    await callback.answer()


@router.callback_query(F.data.startswith("seller_delete_confirm:"))
async def seller_delete_execute(callback: CallbackQuery):
    _, telegram_id = callback.data.split(":")
    seller = get_seller_by_id(int(telegram_id))
    seller_name = seller.get("display_name", "")
    if not seller:
        await callback.answer(seller_not_found_answer(telegram_id), show_alert=True)
        await seller_details_menu_callback(callback)
        return

    if seller.get("seller_status") == "active":
        await callback.answer(
            delete_seller_not_possible_message(seller_name, telegram_id),
            show_alert=True,
        )
        await seller_details_menu_callback(callback)
        return

    try:
        delete_seller_by_id(telegram_id)
        await callback.message.edit_text(
            deleted_seller_confirm_message(telegram_id),
            reply_markup=get_main_menu_keyboard(),
        )
    except Exception as e:
        await callback.message.edit_text(delete_error_message(e))

    await callback.answer()

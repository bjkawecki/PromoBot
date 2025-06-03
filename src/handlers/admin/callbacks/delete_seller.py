from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.repositories.sellers import delete_seller_by_id, get_seller_by_id
from handlers.admin.callbacks.menu import seller_details_menu_callback
from keyboards.admin.manage_seller import (
    get_confirm_delete_seller_keyboard,
)
from keyboards.common import get_main_menu_keyboard
from utils.misc import get_seller_info

router = Router()


@router.callback_query(F.data.startswith("seller_delete:"))
async def seller_delete_confirm(callback: CallbackQuery):
    _, telegram_id = callback.data.split(":")
    seller = get_seller_by_id(int(telegram_id))
    seller_info = get_seller_info(seller)
    keyboard = get_confirm_delete_seller_keyboard(telegram_id)

    await callback.message.edit_text(
        f"❗️<b>Bist du sicher, dass du den folgenden Verkäufer löschen möchtest?</b>\n\n"
        f"{seller_info}",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_delete_seller"))
async def cancel_delete_seller_callback(callback: CallbackQuery):
    await callback.answer("❎ Vorgang abgebrochen.")
    await seller_details_menu_callback(callback)
    await callback.answer()


@router.callback_query(F.data.startswith("seller_delete_confirm:"))
async def seller_delete_execute(callback: CallbackQuery):
    _, telegram_id = callback.data.split(":")
    seller = get_seller_by_id(int(telegram_id))

    if not seller:
        await callback.answer(
            f"❌ Verkäufer mit ID {telegram_id} nicht gefunden.", show_alert=True
        )
        await seller_details_menu_callback(callback)
        return

    if seller.get("status") == "active":
        await callback.answer(
            f"⚠️ Verkäufer mit ID {telegram_id} ist noch aktiv und kann daher nicht gelöscht werden.\n"
            "Bitte deaktiviere ihn zuerst.",
            show_alert=True,
        )
        await seller_details_menu_callback(callback)
        return

    try:
        delete_seller_by_id(telegram_id)
        await callback.message.edit_text(
            f"✅ Verkäufer mit ID {telegram_id} wurde gelöscht.",
            reply_markup=get_main_menu_keyboard(),
        )
    except Exception as e:
        await callback.message.edit_text(f"❌ Fehler beim Löschen: {e}")

    await callback.answer()

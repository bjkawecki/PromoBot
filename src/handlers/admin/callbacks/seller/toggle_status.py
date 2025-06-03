from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.repositories.sellers import get_seller_by_id, save_seller
from handlers.admin.callbacks.seller.menu import seller_details_menu_callback
from keyboards.admin.manage_seller import get_confirm_toggle_keyboard
from utils.misc import get_seller_info

router = Router()


@router.callback_query(F.data.startswith("seller_toggle_is_active:"))
async def seller_toggle_is_active_callback(callback: CallbackQuery):
    _, telegram_id, action = callback.data.split(":")
    seller = get_seller_by_id(int(telegram_id))

    seller_info = get_seller_info(seller)

    confirm_text = (
        "❗️<b>Bist du sicher, dass du den folgenden Verkäufer "
        f"{'aktivieren' if action == 'activate' else 'deaktivieren'} möchtest?</b>\n\n"
        f"{seller_info}"
    )

    keyboard = get_confirm_toggle_keyboard(telegram_id, action)

    await callback.message.edit_text(
        confirm_text, reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_toggle_seller_is_active"))
async def cancel_toggle_callback(callback: CallbackQuery):
    await callback.answer("❎ Vorgang abgebrochen.")
    await seller_details_menu_callback(callback)
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_toggle_seller_is_active:"))
async def confirm_toggle_callback(callback: CallbackQuery):
    _, telegram_id, action = callback.data.split(":")

    seller = get_seller_by_id(int(telegram_id))
    if not seller:
        await callback.message.answer("❌ Verkäufer nicht gefunden.")
        return

    seller["status"] = "active" if action == "activate" else "inactive"
    save_seller(seller)

    status_text = (
        "✅ Verkäufer wurde aktiviert."
        if seller["status"] == "active"
        else "🚫 Verkäufer wurde deaktiviert."
    )
    await callback.answer(status_text)

    await seller_details_menu_callback(callback)
    await callback.answer()

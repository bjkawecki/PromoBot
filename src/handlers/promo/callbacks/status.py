from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.repositories.promos import get_promo_by_id, save_promo
from handlers.promo.callbacks.menu import seller_promo_list_menu_callback
from keyboards.seller.promo import get_confirm_toggle_promo_status_keyboard

router = Router()


@router.callback_query(F.data.startswith("promo_status:"))
async def toggle_promo_status_callback(callback: CallbackQuery):
    _, promo_id, action = callback.data.split(":")

    confirm_text = (
        "❗️<b>Bist du sicher, dass du die Promo "
        f"{'aktivieren' if action == 'a' else 'deaktivieren'} möchtest?</b>\n\n"
    )

    keyboard = get_confirm_toggle_promo_status_keyboard(promo_id, action)

    await callback.message.answer(
        confirm_text, reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_toggle_promo"))
async def cancel_toggle_callback(callback: CallbackQuery):
    await callback.answer("❎ Vorgang abgebrochen.")
    await seller_promo_list_menu_callback(callback)


@router.callback_query(F.data.startswith("confirm_toggle_promo:"))
async def confirm_toggle_callback(callback: CallbackQuery):
    seller_id = callback.from_user.id
    _, promo_id, action = callback.data.split(":")

    promo = get_promo_by_id(promo_id=promo_id, seller_id=seller_id)
    if not promo:
        await callback.message.answer("❌ Promo nicht gefunden.")
        return

    promo["status"] = "active" if action == "a" else "inactive"
    save_promo(promo)

    status_text = (
        "✅ Promo wurde aktiviert."
        if promo["status"] == "active"
        else "🚫 Promo wurde deaktiviert."
    )
    await callback.answer(status_text)

    await seller_promo_list_menu_callback(callback)
    await callback.answer()
